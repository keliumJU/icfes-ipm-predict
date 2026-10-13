"""Worker fijo sin imports de modelos/datos. Exclusivo controles de proceso."""
import sys
import time
mode=sys.argv[1]
if mode=='wait':
    time.sleep(10)
elif mode=='infrastructure':
    sys.exit(3)
elif mode=='numerical':
    sys.exit(2)
elif mode=='success':
    print('resultado inventado; ningún fit')
else:
    sys.exit(4)
