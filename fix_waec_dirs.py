import os
import shutil
import glob

neco_dir = 'data/Academic/Secondary/NECO/Science'
waec_dir = 'data/Academic/Secondary/WAEC/Science'

moved_count = 0
for subj in ['Biology', 'Chemistry']:
    dst_dir = os.path.join(waec_dir, subj)
    os.makedirs(dst_dir, exist_ok=True)
    src_pattern = os.path.join(neco_dir, subj, f'WAEC_{subj}*.md')
    for f in glob.glob(src_pattern):
        dst_file = os.path.join(dst_dir, os.path.basename(f))
        if os.path.exists(dst_file):
            os.remove(dst_file)
        shutil.move(f, dst_dir)
        moved_count += 1

print(f"Successfully moved {moved_count} WAEC files from NECO to WAEC directories.")
