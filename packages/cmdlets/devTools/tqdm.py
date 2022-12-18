# [Imports]
from assets.uilib.tqdm_ui import *

# [Download]
formatting = "{desc}: {percentage:3.0f}% |{color}{bar}{reset}| {n_fmt}/{total_fmt}  {rate_fmt}{postfix}  [Elap: {elapsed} | ETA: {remaining}]"
chars = " " + chr(9592) + chr(9473)
url = "https://github.com/Qalculate/qalculate-qt/releases/download/v4.4.0/qalculate-4.4.0-x64.msi"
downloadBar(url,formatting,chars)