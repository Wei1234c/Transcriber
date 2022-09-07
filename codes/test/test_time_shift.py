from transcriber import SRT, timedelta

fn_srt = 'input.srt'
srt = SRT(fn_srt)

s = srt.get_script(3)
td = timedelta(seconds = 2, microseconds = 48000)
s.time_shift(td)
print()