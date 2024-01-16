# Contributing 

The release process for Bitvavo SDK for Python is semi-automatic. You manually start the GitHub Action that creates 
the SDK package and uploads it to Python package managers.

## Prerequisites

To release the SDK you need to:

- Complete the instructions in the [README Prerequisites](./README.md#prerequisites)

## Release a new version of the SDK

To update the SDK and publish your changes to the Bitvavo developer community:

1. **Make your updates to the SDK**

    Create a branch and implement your changes to the SDK. When you have tested your code updates, make a pull request 
    to the `master` branch.

1. **Create a test package**

   1. When your [pull request](https://github.com/bitvavo/python-bitvavo-api/pulls) is approved, merge your changes to 
      the master branch.
   2. Note the release number of the 
      [latest version of the SDK published to pypi](https://pypi.org/project/python-bitvavo-api/#history)
      and using [semver](https://semver.org/) as your guide, decide on a version number for this release.
   4. In Actions, [run the release action](https://github.com/bitvavo/python-bitvavo-api/actions/workflows/release.yml) 
      using your new release number.
     The release action builds the SDK package and uploads to https://test.pypi.org/project/python-bitvavo-api/.
   
1. **Test the package**

   1. In a [clean virtual environment](https://virtualenv.pypa.io/en/stable/user_guide.html), create a new directory, 
      then download the test package:

       ```python3 -m pip install --index-url https://test.pypi.org/simple/ python-bitvavo-api```

   1. Follow the instructions in [Create a simple Bitvavo implementation](./README.md#get-started) and make a sample 
      app.
       When the functionality you implemented works, the package is good. If you cannot make a 
      call, the debugger is your friend.
   
1. **Publish the SDK**

   1. Open the draft release created when you ran the release action.
   1. Add a brief description about the release.
   
      This description is visible to the world in https://github.com/bitvavo/python-bitvavo-api/releases.
   1. Click **Publish**.

      This starts the Publish action. You see the 
      [new version available on pypi](https://pypi.org/project/python-bitvavo-api/).

Now send the release message in Slack, yay.