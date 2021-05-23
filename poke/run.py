import ctypes
import utils
import sys
import os


def get_heap_range(pid, verbose):
	findc = "cat /proc/%d/maps | grep heap | cut -d '-' -f 1-2" % pid
	h_range = utils.cmd(findc,False).pop().split(' ')[0]
	# convert the string addresses to 16bit integers
	h_start = int(h_range.split('-')[0],16)
	h_stops = int(h_range.split('-')[1],16)
	if verbose:
		print('[+] Heap Ranges: 0x%s-0x%s' % (h_start,h_stops))
	return h_start, h_stops

def extract_heap_memory(l, pid, start, stop, verbose):
	l.attach(pid)
	memfile = '/proc/%d/mem' % pid
	memf = open(memfile, 'rb+')
	memf.seek(start)
	heap_data = memf.read(stop - start)
	memf.close()
	l.detach(pid)
	open('%s.dump'%pid, 'wb+').write(heap_data)
	if verbose:
		print(heap_data)
	return heap_data



def main():
	DEBUG = True
	# Compile Special Library
	if not os.path.isfile('pokelib.so'):
		os.system('gcc -shared -fPIC -o pokelib.so pokelib.c')
	lib = ctypes.cdll.LoadLibrary("./pokelib.so")
	# Get Name of Target Program
	if 3 > len(sys.argv) > 1:
		target_prog = sys.argv[1]
	else:
		target_prog = 'example'
	
	# Get PID of the program 
	target_pid = lib.get_pid(target_prog)

	if '-p' in sys.argv:
		target_pid = int(sys.argv[2])

	# Try to take a peek inside the process id found
	print('[+] Target Program %s has PID: %d' % (target_prog, target_pid))
	# Get Heap location of this PID
	hstart, hstop = get_heap_range(target_pid, DEBUG)
	# Read the /proc/PID/mem file at heap offsets
	hdata = extract_heap_memory(lib, target_pid, hstart, hstop, DEBUG)
	

if __name__ == '__main__':
	main()

