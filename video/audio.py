import json, numpy as np, wave
M = json.load(open("meta.json")); C = M["CUES"]; SR = 44100; DUR = M["TOTAL"]; N = int(SR * DUR)
out = np.zeros(N); rng = np.random.default_rng(7)
def add(sig, t, gain=1.0):
    i = int(t * SR); j = min(N, i + len(sig))
    if i < N: out[i:j] += sig[: j - i] * gain
def env(n, a=.004, r=None):
    t = np.arange(n) / SR; e = np.minimum(1, t / a); return e * (np.exp(-t / r) if r else 1)
def sq(f, dur, soft=True):   # soft square: first odd harmonics only
    t = np.arange(int(SR * dur)) / SR; ph = 2 * np.pi * (np.cumsum(f if np.ndim(f) else np.full_like(t, f)) / SR if np.ndim(f) else f * t)
    return np.sin(ph) + np.sin(3 * ph) / 3 + np.sin(5 * ph) / 5 * (0 if soft else 1)
def blip(f, dur=.05, gain=.06): s = sq(f, dur) * env(int(SR * dur), .002, dur / 3); return s * gain
def click(gain=.05): n = int(SR * .004); s = rng.standard_normal(n) * env(n, .0005, .001); s = np.diff(s, prepend=0); return s * gain
def kick(gain=.33, big=False):
    d = .35 if big else .2; t = np.arange(int(SR * d)) / SR; f = 45 + 55 * np.exp(-t / .03); ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) * np.exp(-t / (.16 if big else .09)) * gain
def hat(gain=.025): n = int(SR * .03); s = np.diff(rng.standard_normal(n + 1)) * env(n, .001, .008); return s * gain
def chime(gain=.09):
    a = blip(784, .1, gain); b = blip(1175, .16, gain); s = np.zeros(int(SR * .3)); s[:len(a)] += a; k = int(SR * .1); s[k:k + len(b)] += b; return s
def bwomp(gain=.07):
    d = .28; t = np.arange(int(SR * d)) / SR; f = 300 * np.exp(-t / .12) + 90; ph = 2 * np.pi * np.cumsum(f) / SR
    return (np.sin(ph) + np.sin(3 * ph) / 3) * np.exp(-t / .1) * gain
# pad: A minor-ish drone, fades in, lifts at the intro, fades out
t = np.arange(N) / SR
pad = sum(np.sin(2 * np.pi * f * t + ph) * g for f, g, ph in [(55, .5, 0), (82.41, .35, 1), (110, .3, 2), (164.81, .14, .5), (220, .06, 1.3)])
lvl = np.interp(t, [0, 1.5, 7.4, 8.2, DUR - 2.0, DUR], [0, .035, .035, .055, .055, 0]) * (1 + .15 * np.sin(2 * np.pi * .23 * t))
out += pad * lvl
# typing
a, b = C["typeA"]; [add(click(.05 * rng.uniform(.6, 1)), a + k / 22) for k in range(int((b - a) * 22))]
a, b = C["typeB"]; [add(click(.045 * rng.uniform(.6, 1)), a + k / 23) for k in range(int((b - a) * 23))]
# the bag filling in, block by block
a, b = C["fill"]; [add(blip(220 * 2 ** (k / 13), .045, .045), a + (b - a) * k / 12) for k in range(13)]
add(bwomp(.06), C["reveal"][0])
for s_ in C["sells"]: add(bwomp(.08), s_); add(kick(.18), s_)
# the beat: from the intro to the end card
bt = 7.6
while bt < 21.55: add(kick(.3), bt); bt += .5
bt = 11.85
while bt < 21.55: add(hat(.022), bt); bt += .5
add(chime(.06), C["intro"][2]); add(chime(.08), C["cleanF"][0])
add(chime(.1), C["cleanBoard"][0])
for k, s_ in enumerate(C["ticks"]): add(blip(880 * 2 ** (k / 12), .05, .05), s_)
add(chime(.12), C["cleanChip"][0]); add(kick(.35, True), C["cleanChip"][0])
for s_ in C["engine"]: add(blip(660, .04, .035), s_)
# the end card
e0, e1, e2 = C["end"]; add(kick(.45, True), e0)
stab = sum(np.sin(2 * np.pi * f * np.arange(int(SR * 2.4)) / SR) for f in (220, 277.18, 329.63, 440)) * np.exp(-np.arange(int(SR * 2.4)) / SR / .9) * .03
add(stab, e0); add(chime(.11), e1); add(blip(1046, .07, .06), e2)
out = np.tanh(out * 1.2) / np.tanh(1.2)
out *= .89 / max(1e-9, np.abs(out).max())
fade = np.ones(N); k = int(SR * .6); fade[-k:] = np.linspace(1, 0, k); out *= fade
pcm = (out * 32767).astype(np.int16); st = np.repeat(pcm[:, None], 2, axis=1)
w = wave.open("audio.wav", "wb"); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(st.tobytes()); w.close()
print("audio", DUR, "s")
