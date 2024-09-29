default:
	/usr/bin/env python src/unicodef.py defs outfiles

install:
	mkdir -p ~/.unicodef \
		&& cp -p outfiles/* ~/.unicodef

macosinstall: install
	mkdir -p ~/Library/KeyBindings \
		&& rm -f ~/Library/KeyBindings/DefaultKeyBinding.dict \
		&& cp -f ~/.unicodef/unicodefs.dict ~/Library/KeyBindings/DefaultKeyBinding.dict

uninstall:
	rm -rf ~/.unicodef

macosuninstall: uninstall
	rm -i ~/Library/KeyBindings/DefaultKeyBinding.dict

clean:
	rm -f outfiles/*

