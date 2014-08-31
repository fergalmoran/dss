from azure.storage import BlobService
from azure import WindowsAzureMissingResourceError
from django.core.management.base import NoArgsCommand
from django.utils.encoding import smart_str
from dss.storagesettings import AZURE_ACCOUNT_NAME, AZURE_ACCOUNT_KEY, AZURE_CONTAINER
from spa.models import Mix


class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        try:
            blob_service = BlobService(AZURE_ACCOUNT_NAME, AZURE_ACCOUNT_KEY)
            mixes = Mix.objects.all()
            for mix in mixes:
                try:
                    blob_name = "%s.%s" % (mix.uid, mix.filetype)
                    blob = blob_service.get_blob(AZURE_CONTAINER, blob_name)
                    if blob:
                        download_name = smart_str('Deep South Sounds - %s.%s' % (mix.title, mix.filetype))
                        blob_service.set_blob_properties(
                            AZURE_CONTAINER,
                            blob_name,
                            x_ms_blob_content_type='application/octet-stream',
                            x_ms_blob_content_disposition='attachment;filename="%s"' % download_name
                        )
                        print "Processed: %s" % mix.uid
                    else:
                        print "No blob found for: %s" % mix.uid
                except WindowsAzureMissingResourceError:
                    print "No blob found for: %s" % mix.uid

        except Exception, ex:
            print "Error processing blobs: %s" % ex.message


def _test_set_header(self):
    try:
        blob_service = BlobService(AZURE_ACCOUNT_NAME, AZURE_ACCOUNT_KEY)
        blobs = blob_service.list_blobs(AZURE_CONTAINER)
        for blob in blobs:
            blob_service.set_blob_properties(
                AZURE_CONTAINER,
                blob.name,
                x_ms_blob_content_type='application/octet-stream',
                x_ms_blob_content_disposition='attachment;filename="Arg.mp3"'
            )
            print "Got properties"

    except Exception, ex:
        print "Debug exception: %s" % ex.message