default:
	cd src \
		&& sh unicodef.sh ../defs/* \
		&& cp -p build/*.md build/*.XCompose build/*.vim build/*.yaml ../outfiles/

macos: default
	cd src \
		&& python3 gencompose.py build/unicodefs.yaml > build/DefaultKeyBinding.dict \
		&& cp -p build/DefaultKeyBinding.dict ../outfiles/DefaultKeyBinding.dict

install:
	mkdir -p ~/.unicodef \
		&& cp -p outfiles/* ~/.unicodef

macosinstall:
	mkdir -p ~/Library/KeyBindings \
		&& cp -p outfiles/DefaultKeyBinding.dict ~/Library/KeyBindings

uninstall:
	rm -rf ~/.unicodef

clean:
	rm -rf src/build

cleanall: clean
	rm -f outfiles/*
