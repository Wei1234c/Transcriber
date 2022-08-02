from transcriber import SRT

fn_srt = 'test.srt'
srt = SRT(fn_srt)

print(srt.get_script(3))
print(srt.get_script(4))
print(srt.get_script(5))
# print(srt.merge_two_scripts(3, 4, True))

print(srt.merge (3, 4, 5))
print(srt.scripts[:8])
srt.dump('test1.txt')