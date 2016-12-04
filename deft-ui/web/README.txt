Please note that when you run the development server, it needs to have the correct python path.

For example, in my case, I do:
export PYTHONPATH=/afs/cern.ch/user/m/mpotekhi/panda-deft/deft-ui/trunk/web/utils:$PYTHONPATH

You should be able to figure out a way to set the path so all components can be picked up by Django.

When we move to Apache, there will need to be a correct path defined within the httpd.conf file.
