"""Original short reaction sounds, generated locally by FFmpeg."""
import re


TONES = {
    "boom": ("62*t+5*(1-exp(-24*t))", 0.65),
    "boing": ("220*t+1.6*sin(31*t)*exp(-4*t)", 0.55),
    "falling_whistle": ("1200*t-650*t*t", 0.78),
    "pop": ("780*t-3000*t*t", 0.10),
    "question": ("490*t+440*t*t", 0.32),
    "fail_horn": ("165*t-42*t*t+0.20*sin(2*PI*330*t)", 0.62),
    "sparkle": ("1120*t+0.7*sin(2*PI*560*t)", 0.38),
    "spring": ("330*t+1.2*sin(54*t)*exp(-3*t)", 0.39),
    "glitch": ("240*t+0.8*sin(2*PI*57*t)", 0.20),
    "bell": ("740*t+1.5*sin(2*PI*1030*t)*exp(-12*t)", 0.55),
}


def audio_filter(clip, words, start, end):
    tone = TONES.get(clip.get("reaction"))
    anchor = re.findall(r"\w+", str(clip.get("reaction_phrase", "")).casefold())
    if not tone or not 2 <= len(anchor) <= 8:
        return None
    tokens = [(token, word["e"]) for word in words if start <= word["s"] < end
              for token in re.findall(r"\w+", word["w"].casefold())]
    text = [token for token, _ in tokens]
    matches = [index for index in range(len(tokens) - len(anchor) + 1)
               if text[index:index + len(anchor)] == anchor]
    if len(matches) != 1:
        return None
    phase, duration = tone
    offset = tokens[matches[0] + len(anchor) - 1][1] - start
    if offset < 0 or offset + duration > end - start:
        return None
    return (f"aevalsrc='0.13*sin(2*PI*({phase}))*exp(-3*t/{duration})':s=48000:d={duration},"
            f"afade=t=in:d=0.008,afade=t=out:st={duration - 0.045}:d=0.045,"
            f"adelay={round(offset * 1000)}:all=1[cue]")
