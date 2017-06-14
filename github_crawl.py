'''
This script fetches Java code samples from github repositories. We make
use of github search API to find repos containing Java language code. Then,
we search for Java source files in each repo found in previous query.
No. of source files to take from each repo can be limited via a parameter.
The source files are saved locally in a folder named src_data under the
directory in which this script is executed.

__author__ = "B. Sodhi"
__credits__ = ["stackoverflow.com","google search engine"]
__license__ = "MIT"
__version__ = "0.1"

'''

import requests, base64
import sys, traceback, os, time


def fetch_code_from_repo(repo):
    '''
    Fetches Java source code files via an empty search string query in the
    given repository. Fetched files are saved in src_data subdirectory.
    :param repo: JSON object representing the github repository to be
    searched for Java code.
    :return: Number of files fetched.
    '''
    file_count = 0
    url_code = "https://api.github.com/search/code?q=+in:file+language:java+repo:"

    try:
        repo_name = repo['full_name']
        name = repo['name']
        print "Processing files from repo " + repo_name
        res2 = requests.get(url_code + repo_name)
        if res2.status_code != 200:
            print("Failed to read from repo " + repo_name + ". " + res2.text)
            return file_count

        codes = res2.json()['items']

        for c in codes:
            try:
                # Unauthenticated API call rate limit is 10 requests/minute,
                # so we sleep for 7 seconds between successive requests.
                time.sleep(7)

                file_name = c['name']
                if "package-info.java" == file_name:
                    continue
                print "Fetching " + c['git_url']
                res_git = requests.get(c['git_url'])
                if res_git.status_code != 200:
                    print("Failed to read. " + res_git.text)
                    continue

                code = res_git.json()

                # Ignore files smaller than ~1kB and bigger than 6kB in size
                if code['size'] < 1000 or code['size'] > 6000:
                    print "Discarded because size not in range."
                    continue

                print "Code size: " + str(code['size'])
                text = base64.b64decode(code['content'])

                directory = 'src_data'
                if not os.path.exists(directory):
                    os.makedirs(directory)

                with open(directory + '/' + repo_name.replace('/', '_') + "_" + file_name, "w") as text_file:
                    text_file.write(text)
                file_count += 1
                # Limit the no. of files to take from each repo
                if file_count == 50:
                    break
                file_count += 1

            except Exception:
                print("Error occurred when processing code item. Skipping to next.")
                print(traceback.format_exc())

    except Exception:
        print("Could not process repo item. Skipping to next repo.")
        print(traceback.format_exc())

    return file_count


def process_repos():
    '''
    Searches for github repositories that contain Java source code files.
    github search API is used to find such repositories.
    :return:
    '''
    print "Fetching github repos info ..."
    url_repo = "https://api.github.com/search/repositories?q=+language:java"
    res = requests.get(url_repo)

    if res.status_code != 200:
        print("Could not complete HTTP request. " + res.text)
        return

    jres = res.json()
    repos = jres['items']

    repo_count = 0
    total_files = 0

    print "Found {0} repositories.".format(len(repos))

    for r in repos:
        repo_count += 1
        total_files += fetch_code_from_repo(r)

    print "Total {0} files processed from {1} repositories.".format(total_files, repo_count)

# Call the main function
def main(argv):
    process_repos()

if __name__ == "__main__":
    main(sys.argv)