# Extract Facebook Messenger Attachments

This script will parse through all your sent and received Facebook messenger messages and extract all photos and videos, both sent and received.
All attachments will be tagged with their "creation date" according to the message log, this seems to indicates when the image was uploaded to Facebook.

**This script will not modify your source data it will only create copies of the original data with new names and metadata**

## How to use it

- Request your data from Facebook, make sure you request your message history.
- Wait for your data to be ready, download and extract your data to a folder.

```bash
git clone ...
cd extract-fb-images
```
- From your facebook data folder, copy/move the `inbox` folder into the `place-inbox-here`.
- Run the script
```bash
python3 ./extractImages.py
```
- All your images should eventually end up the output folder, inside a folder named after the date and time you extracted the data.