# gactions-computer-controller

This is a django app to power a basic home media PC. It can response to requests from a Google Assistant App to play video files and open web pages.

## Setup
### Setting up a Google Assistant development project
- Get the django application running on a https server, and edit `google/action.json` to set the IP of this machine.
- Create a Google Assitant development project, with Actions SDK: https://developers.google.com/actions/sdk/
- Using the `gactions` application from Google run the following command from with the `google` folder:

        `./gactions test --action_package action.json --project YOUR_TEST_PROJECT`

### Run the listener
The listener should be run as your normal user, which will have access to your X server, in order to run applications like vlc. This is needed so you don't have to grant `www-data` any additional permissions. To run the listener just run the bash script `listener/listener.bash`.
