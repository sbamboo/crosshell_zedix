# [Imports]
from assets.lib.tqdm_ui import *

# [Download]
formatting = "{desc}: {percentage:3.0f}% |{color}{bar}{reset}| {n_fmt}/{total_fmt}  {rate_fmt}{postfix}  [Elap: {elapsed} | ETA: {remaining}]"
chars = " " + chr(9592) + chr(9473)
url = "https://github.com/simonkalmiclaesson/packagehand_repository/raw/main/packages/cmdlet/crosshell.packagehandTesting/latest.package"
url = "https://github.com/simonkalmiclaesson/packagehand_repository/raw/main/repository/cmdlet/_thirdpartyimports/qualculate/qalculate_latest_win.package"
downloadBar(url,formatting,chars)