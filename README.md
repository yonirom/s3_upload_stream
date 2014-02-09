AWS S3 Stream uploader
======================

Uploads a stream to S3

Requirements: 
-------------
* boto



Usage example:
--------------

tar cvfp - / | s3_stream_writer.py -b mybucket -f system_backup.tar
