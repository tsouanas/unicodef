default:
	cd src \
		&& sh unicodef.sh ../defs/* \
		&& cp -p build/*.md build/*.XCompose build/*.vim build/*.yaml ../outfiles/ \
		&& cat macOS.yaml build/unicodefs.yaml | /usr/bin/env python3 gencompose.py - | sed -f macOSescape.sed > build/unicodefs.dict \
		&& cp -p build/unicodefs.dict ../outfiles/

nomacos:
	cd src \
		&& sh unicodef.sh ../defs/* \
		&& cp -p build/*.md build/*.XCompose build/*.vim build/*.yaml ../outfiles/

install:
	mkdir -p ~/.unicodef \
		&& cp -p outfiles/* ~/.unicodef

macosinstall: install
	mkdir -p ~/Library/KeyBindings \
		&& cp -f ~/.unicodef/unicodefs.dict ~/Library/KeyBindings/DefaultKeyBinding.dict

uninstall:
	rm -rf ~/.unicodef

macosuninstall: uninstall
	rm -i ~/Library/KeyBindings/DefaultKeyBinding.dict

clean:
	rm -rf src/build

cleanall: clean
	rm -f outfiles/*
