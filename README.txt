Usage: Paster.py [Options] file

Splits a file into chunks, base64 encodes those chunks and uploads them to
various pastebins. Original idea from pyCloudForce

Options:
  -h, --help            show this help message and exit
  -m MODE, --mode=MODE  action to use 'push' files/'pull'reconstruct files
  -c CHUNKS, --chunks=CHUNKS
                        How many chunks you wish to split the file
                        into(Default 2)
  -o OUTPUT, --output=OUTPUT
                        Output file that holds the links to your spread data
  -s SLEEP_TIME, --sleep=SLEEP_TIME
                        Time to wait before pushing the next chunk(Default 3)
