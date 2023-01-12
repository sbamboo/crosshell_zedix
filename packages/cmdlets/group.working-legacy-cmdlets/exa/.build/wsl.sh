sudo apt update
sudo apt install python3
sudo apt install python3-pip
curl https://sh.rustup.rs -sSf | sh
rustup target add x86_64-pc-windows-gnu
cp ./config ~/.cargo/config
sudo apt-get install gcc-mingw-w64-x86-64 -y
rustup target add x86_64-pc-windows-gnu
sudo apt-get install libsdl2-dev -y
curl -s https://www.libsdl.org/release/SDL2-devel-2.0.9-mingw.tar.gz | tar xvz -C /tmp
mkdir -p ~/projects
cd ~/projects
git clone https://github.com/Rust-SDL2/rust-sdl2
cd rust-sdl2
cp -r /tmp/SDL2-2.0.9/x86_64-w64-mingw32/lib/* ~/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/rustlib/x86_64-pc-windows-gnu/lib/
cp /tmp/SDL2-2.0.9/x86_64-w64-mingw32/bin/SDL2.dll .
cargo build --target=x86_64-pc-windows-gnu
cd target
cd x86_64-pc-windows-gnu
cd debug
copy ./exa.exe ./../../../../exa.exe
cd ./../../../..
rmdir -r ./exa/ -f