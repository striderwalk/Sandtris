# profiler for project
import cProfile
import os
import pstats

from main import main

print("timeing started please DON'T press anything")
with cProfile.Profile() as pr:
    main()
print("timeing ended")

st = pstats.Stats(pr)
st.sort_stats(pstats.SortKey.TIME)
st.print_stats()

st.dump_stats(filename="assets/data.prof")
os.system("snakeviz assets/data.prof")
