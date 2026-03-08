import secrets
import matplotlib.pyplot as plt

# Public parameters (P is prime, G is generator, Q = P-1 is group order)
P = 2267
G = 2
Q = P - 1


# Prover chooses random r and sends t = g^r mod p
# This hides the secret but starts the proof
class Prover:
    def __init__(self, secret: int):
        self._x = secret % Q              
        self.Y = pow(G, self._x, P)       

    def commit(self):
        self._r = secrets.randbelow(Q - 1) + 1
        return pow(G, self._r, P)       

    def respond(self, c: int):
        return (self._r + c * self._x) % Q  

# Fake prover does NOT know x, so it cannot compute s = r + x if c = 1. The goal here is to cheat and get accepted anyway. Hence, it will guess the verifier’s 
# challenge in advance (we are calling it c_guess). Firstly, we pick random s (this is what the fake prover will send as a response). Then c_guess as 0 or 1. Then we get 
# t = g^s . (y^c_guess) ^ -1 mod p (This equation produces the correct t if c = c_guess). Hence the fake prover's success probability = 1/2 per round. 
# For n rounds, the fake prover must guess all challenges correctly
class FakeProver:
    def __init__(self, Y: int):
        self.Y = Y

    def commit(self):
        self._s = secrets.randbelow(Q - 1) + 1
        self._c_guess = secrets.randbelow(2)
        Yc_inv = pow(pow(self.Y, self._c_guess, P), P - 2, P)
        return (pow(G, self._s, P) * Yc_inv) % P

    def respond(self, c: int):
        return self._s                  

# Verifier sends random c in {0, 1}and checks g^s == t * y^c mod p
# If c=0, the equation s = (r + c*x) mod Q becomes s=r, verifier checks G^r = t, which always passes. If s = r+x, verifier checks G^(r+x), 
# hence the prover that knows x can only pass this. 
# The fake prover doesn't know x, and can only guess c. If the guessed matches the actual, only then it can surpass the verifier. 
# When running this multiple times, it becomes exponentially harder for the fake prover. That’s why more rounds make cheating practically impossible.
class Verifier:
    def __init__(self, Y: int):
        self.Y = Y

    def challenge(self, t: int):
        self._t = t
        self._c = secrets.randbelow(2)
        return self._c

    def verify(self, s: int):
        lhs = pow(G, s, P)
        rhs = (self._t * pow(self.Y, self._c, P)) % P
        return lhs == rhs


def run_round(prover, verifier):
    t = prover.commit()
    c = verifier.challenge(t)
    s = prover.respond(c)
    return verifier.verify(s)


def acceptance_rate(prover, verifier, trials=500):
    return sum(run_round(prover, verifier) for _ in range(trials)) / trials



SECRET = 1337
honest = Prover(SECRET)
fake   = FakeProver(honest.Y)
v      = Verifier(honest.Y)


print("Honest Prover Demo (5 rounds)")
for i in range(1, 6):
    result = run_round(honest, v)
    print(f"  Round {i}: {'ACCEPT' if result else 'REJECT'}")


print("\nFake Prover Demo (5 rounds)")
for i in range(1, 6):
    result = run_round(fake, v)
    print(f"  Round {i}: {'ACCEPT' if result else 'REJECT'}")


print("\nAcceptance Rate vs Rounds (500 trials each)")
print(f"{'Rounds':>8} | {'Honest':>8} | {'Fake':>8} | {'Theory':>8}")
print("-" * 40)

rounds_list  = list(range(1, 17))
fake_rates   = []
honest_rates = []

for n in rounds_list:
    def multi_round(prover, verifier, n=n):
        return all(run_round(prover, verifier) for _ in range(n))

    h = sum(multi_round(honest, v) for _ in range(500)) / 500
    f = sum(multi_round(fake,   v) for _ in range(500)) / 500
    theory = 0.5 ** n

    honest_rates.append(h)
    fake_rates.append(f)
    print(f"{n:>8} | {h:>7.1%} | {f:>7.2%} | {theory:>7.2%}")


theory_rates = [0.5 ** n for n in rounds_list]

plt.figure(figsize=(9, 5))
plt.plot(rounds_list, [r * 100 for r in honest_rates], 'o-', label='Honest prover')
plt.plot(rounds_list, [r * 100 for r in fake_rates],   's-', label='Fake prover')
plt.xlabel('Number of rounds')
plt.ylabel('Acceptance rate (%)')
plt.title('ZKP: Acceptance Rate vs Number of Rounds')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('zkp_plot.png', dpi=150)
plt.show()
print("\nPlot saved to zkp_plot.png")