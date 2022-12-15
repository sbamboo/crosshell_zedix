# [Imports]
from time import sleep
try:
    from tqdm import tqdm
except:
    os.system("pip3 install tqdm")
    from tqdm import tqdm
try:
    import requests
except:
    os.system("pip3 install requests")
    import requests
try:
    from urllib.request import urlopen
except:
    os.system("pip3 install urllib")
    from urllib.request import urlopen


# [Test loadingbar]
def download(url, formatting="{l_bar}{color}{bar}{reset}{r_bar}", chars=None, ncolsi=110, uniti='iB', block_size=1024,):
    colorList = ['\x1b[38;2;0;255;0;1m', '\x1b[38;2;3;252;0;1m', '\x1b[38;2;5;250;0;1m', '\x1b[38;2;8;247;0;1m', '\x1b[38;2;10;245;0;1m', '\x1b[38;2;13;242;0;1m', '\x1b[38;2;15;240;0;1m', '\x1b[38;2;18;237;0;1m', '\x1b[38;2;21;234;0;1m', '\x1b[38;2;23;232;0;1m', '\x1b[38;2;26;229;0;1m', '\x1b[38;2;28;227;0;1m', '\x1b[38;2;31;224;0;1m', '\x1b[38;2;33;222;0;1m', '\x1b[38;2;36;219;0;1m', '\x1b[38;2;39;216;0;1m', '\x1b[38;2;41;214;0;1m', '\x1b[38;2;44;211;0;1m', '\x1b[38;2;46;209;0;1m', '\x1b[38;2;49;206;0;1m', '\x1b[38;2;52;203;0;1m', '\x1b[38;2;54;201;0;1m', '\x1b[38;2;57;198;0;1m', '\x1b[38;2;59;196;0;1m', '\x1b[38;2;62;193;0;1m', '\x1b[38;2;64;191;0;1m', '\x1b[38;2;67;188;0;1m', '\x1b[38;2;70;185;0;1m', '\x1b[38;2;72;183;0;1m', '\x1b[38;2;75;180;0;1m', '\x1b[38;2;77;178;0;1m', '\x1b[38;2;80;175;0;1m', '\x1b[38;2;82;173;0;1m', '\x1b[38;2;85;170;0;1m', '\x1b[38;2;88;167;0;1m', '\x1b[38;2;90;165;0;1m', '\x1b[38;2;93;162;0;1m', '\x1b[38;2;95;160;0;1m', '\x1b[38;2;98;157;0;1m', '\x1b[38;2;100;155;0;1m', '\x1b[38;2;103;152;0;1m', '\x1b[38;2;106;149;0;1m', '\x1b[38;2;108;147;0;1m', '\x1b[38;2;111;144;0;1m', '\x1b[38;2;113;142;0;1m', '\x1b[38;2;116;139;0;1m', '\x1b[38;2;118;137;0;1m', '\x1b[38;2;121;134;0;1m', '\x1b[38;2;124;131;0;1m', '\x1b[38;2;126;129;0;1m', '\x1b[38;2;129;126;0;1m', '\x1b[38;2;131;124;0;1m', '\x1b[38;2;134;121;0;1m', '\x1b[38;2;137;118;0;1m', '\x1b[38;2;139;116;0;1m', '\x1b[38;2;142;113;0;1m', '\x1b[38;2;144;111;0;1m', '\x1b[38;2;147;108;0;1m', '\x1b[38;2;149;106;0;1m', '\x1b[38;2;152;103;0;1m', '\x1b[38;2;155;100;0;1m', '\x1b[38;2;157;98;0;1m', '\x1b[38;2;160;95;0;1m', '\x1b[38;2;162;93;0;1m', '\x1b[38;2;165;90;0;1m', '\x1b[38;2;167;88;0;1m', '\x1b[38;2;170;85;0;1m', '\x1b[38;2;173;82;0;1m', '\x1b[38;2;175;80;0;1m', '\x1b[38;2;178;77;0;1m', '\x1b[38;2;180;75;0;1m', '\x1b[38;2;183;72;0;1m', '\x1b[38;2;185;70;0;1m', '\x1b[38;2;188;67;0;1m', '\x1b[38;2;191;64;0;1m', '\x1b[38;2;193;62;0;1m', '\x1b[38;2;196;59;0;1m', '\x1b[38;2;198;57;0;1m', '\x1b[38;2;201;54;0;1m', '\x1b[38;2;203;52;0;1m', '\x1b[38;2;206;49;0;1m', '\x1b[38;2;209;46;0;1m', '\x1b[38;2;211;44;0;1m', '\x1b[38;2;214;41;0;1m', '\x1b[38;2;216;39;0;1m', '\x1b[38;2;219;36;0;1m', '\x1b[38;2;222;33;0;1m', '\x1b[38;2;224;31;0;1m', '\x1b[38;2;227;28;0;1m', '\x1b[38;2;229;26;0;1m', '\x1b[38;2;232;23;0;1m', '\x1b[38;2;234;21;0;1m', '\x1b[38;2;237;18;0;1m', '\x1b[38;2;240;15;0;1m', '\x1b[38;2;242;13;0;1m', '\x1b[38;2;245;10;0;1m', '\x1b[38;2;247;8;0;1m', '\x1b[38;2;250;5;0;1m', '\x1b[38;2;252;3;0;1m', '\x1b[38;2;255;0;0;1m']
    colorList.reverse()
    filename = url.split("/")[-1]
    print(f"Downloading {filename}...")
    site = urlopen(url)
    meta = site.info()
    # Streaming, so we can iterate over the response.
    response = requests.get(url, stream=True)
    total_size_in_bytes = int(meta["Content-Length"])
    if chars != None and chars != "":
        progress_bar = tqdm(total = total_size_in_bytes, unit=uniti, unit_scale=True, ncols=ncolsi, ascii=chars)
    else:
        progress_bar = tqdm(total = total_size_in_bytes, unit=uniti, unit_scale=True, ncols=ncolsi)
    with open(filename, 'wb') as file:
        color = ""
        for data in response.iter_content(block_size):
            progress_bar.update(len(data))
            file.write(data)
            procentA = int(str(progress_bar).strip(" ").split("%")[0])
            if int(procentA-1) <= int(len(colorList)):
                color = colorList[procentA-1]
            else: color = colorList[0]
            formatting = formatting.replace("{reset}","\033[0m")
            if "{color}" in formatting:
                p1 = str(formatting.split("{color}")[0])
                p2 = str(''.join(formatting.split("{color}")[1:]))
                progress_bar.bar_format = p1 + color + p2
            else:
                progress_bar.bar_format = formatting.replace("{color}",color)
    progress_bar.close()

formatting = "{desc}: {percentage:3.0f}% |{color}{bar}{reset}| {n_fmt}/{total_fmt}  {rate_fmt}{postfix}  [Elap: {elapsed} | ETA: {remaining}]"
chars = " " + chr(9592) + chr(9473)
url = "https://github.com/Qalculate/qalculate-qt/releases/download/v4.4.0/qalculate-4.4.0-x64.msi"
download(url,formatting,chars)