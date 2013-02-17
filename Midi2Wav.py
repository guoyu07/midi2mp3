import midifetch, subprocess, os
import cloudfiles

class Midi2WavConverter:
	def __init__(self,api_username,api_key,api_bucket,outputfolder = "."):
		self.outputfolder = outputfolder
		self.conn = cloudfiles.get_connection(username=api_username, api_key=api_key,timeout=30)
		self.music_container = None
		containers = self.conn.get_all_containers()
		for container in containers:
		    if container.name == api_bucket:
			self.music_container = container
			break
		
	def __del__(self):
		try:
			self.conn.close()
		except:
			pass

	def convert(self,productid):
		print "Fetching midi"
		midifetch.fetchMidi(productid)

		print "Calling fluidsynth"
		subprocess.call(['fluidsynth','-l','-i','-a', 'file','-z','2048','PC51d.sf2', str(productid) + ".mid"])
		f= str(productid) + ".mp3"
		subprocess.call(['sox','fluidsynth.wav',f])

		print "Uploading to cloudfiles"

		my_music = self.music_container.create_object(f)
		my_music.load_from_filename(os.path.join(self.outputfolder,f))
		print "Done"

if __name__ == '__main__':
	import argparse, json
	parser = argparse.ArgumentParser(
		description="Simple argument parser")
	parser.add_argument("-payload", type=str, required=False,
		help="The location of a file containing a JSON payload.")
	parser.add_argument("-d", type=str, required=False,
		help="Directory")
	parser.add_argument("-e", type=str, required=False,
		help="Environment")
	parser.add_argument("-id", type=str, required=False,
		help="Task id")
	args = parser.parse_args()

	if args.payload is not None:
		payload = json.loads(open(args.payload).read())
		if 'ids' in payload:
			ids = payload['ids']
		if 'api_username' in payload:
			api_username = payload['api_username']
		if 'api_key' in payload:
			api_key = payload['api_key']

	if args.d is not None:
		outputfolder = args.d
	else:	
		outputfolder = "."
	
	converter = Midi2WavConverter(api_username,api_key,"mp3s",outputfolder)
	if ids is not None:
		for id in ids:
			converter.convert(int(id))
