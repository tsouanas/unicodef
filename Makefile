default:
	cd src \
		&& sh unicodef.sh ../defs/* \
		&& cp -p build/*.md build/*.XCompose build/*.vim build/*.yaml ../outfiles/

install:
	mkdir -p ~/.unicodef \
		&& cp -p outfiles/* ~/.unicodef

uninstall:
	rm -rf ~/.unicodef

clean:
	rm -rf src/build

cleanall: clean
	rm -f outfiles/*
