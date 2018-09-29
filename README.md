# cpcb-downloader
Comprehensive scripts to download and arrange pollution data into proper csvs. All data collected from cpcb.nic.in.

Uses the APIs to fetch data in JSON unlike the other available scripts. 

### Requirements

curl on Linux (this program doesn't seem to mess well with the windows version of curl)
python3
pandas

## Instructions v0.1

### Downloading data

1. Open up the file `cpcb_json_downloader.py`.

2. Modify the contents of the code under `if __name__ == '__main__':` block.

...The code here is mostly self-descriptive. The helper function  may be called along with the arguments (SiteID, Month(mm), Year(yy)) or, alternatively, the loop at the end can be used to download data for multiple sites, multiple months, for multiple years in a single iteration.

3. Keep an eye out for files of low size. More often than not, either they could not be properly downloaded, or the data doesn't exist at all. 

### Merging/Arranging data

1.  Open up `json_merger_year.py`.

2. Modify variables `root` and `sites_arr` as required.

3. Run the script.

