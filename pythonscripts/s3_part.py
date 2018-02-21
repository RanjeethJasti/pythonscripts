#!/usr/bin/python
import os, sys
import math
import boto

AWS_ACCESS_KEY_ID = 'AKIAJ6MVAAU7LSJIQO3Q'
AWS_SECRET_ACCESS_KEY = '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'

def upload_file(s3, bucketname, file_path):

        b = s3.get_bucket(bucketname)

        filename = os.path.basename(file_path)
        k = b.new_key(filename)

        mp = b.initiate_multipart_upload(filename)

        source_size = os.stat(file_path).st_size
        bytes_per_chunk = 10000000
        chunks_count = int(math.ceil(source_size / float(bytes_per_chunk)))

        for i in range(chunks_count):
                #print "Iteration - " + str(i)
                offset = i * bytes_per_chunk
                #print "offset" + str(offset)
                remaining_bytes = source_size - offset
                #print "remaining bytes" + str(remaining_bytes)
                bytes = min([bytes_per_chunk, remaining_bytes])
                part_num = i + 1

                print "uploading part " + str(part_num) + " of " + str(chunks_count)

                with open(file_path, 'r') as fp:
                        fp.seek(offset)
                        mp.upload_part_from_file(fp=fp, part_num=part_num, size=bytes)

        if len(mp.get_all_parts()) == chunks_count:
                mp.complete_upload()
                print "upload_file done"
        else:
                mp.cancel_upload()
                print "upload_file failed"

if __name__ == "__main__":

        if len(sys.argv) != 3:
                print "usage: python s3_part.py bucketname filepath"
                exit(0)

        bucketname = sys.argv[1]

        filepath = sys.argv[2]

        s3 = boto.connect_s3(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)

        upload_file(s3, bucketname, filepath)
