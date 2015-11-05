#! /bin/bash

if [ "$PARSEC_APPS_PATH" == "" ]; then
    echo "ERROR: env variable PARSEC_APPS_PATH not defined. Please define it to point to the parsec pkgs/apps dir."
    exit 1
fi

function pushd_silent {                                                                   
    pushd "$@" > /dev/null
}

function popd_silent {                                                                   
    popd "$@" > /dev/null
}

echo -n "Preparing blackscholes..."
pushd_silent $PARSEC_APPS_PATH/blackscholes/inputs
tar xf input_simsmall.tar
tar xf input_simmedium.tar
tar xf input_simlarge.tar
popd_silent
echo "DONE"

echo -n "Preparing fluidanimate..."
pushd_silent $PARSEC_APPS_PATH/fluidanimate/inputs
tar xf input_simsmall.tar
tar xf input_simmedium.tar
tar xf input_simlarge.tar
pushd_silent
echo "DONE"

echo -n "Preparing facesim..."
pushd_silent $PARSEC_APPS_PATH/facesim/inst/amd64-linux.gcc
rm -rf bin-sm/
rm -rf bin-md/
rm -rf bin-lg/
cp -rf bin/ bin-sm/
cp -rf bin/ bin-md/
cp -rf bin/ bin-lg/
popd_silent
pushd_silent $PARSEC_APPS_PATH/facesim/inputs
tar xf input_simsmall.tar -C $PARSEC_APPS_PATH/facesim/inst/amd64-linux.gcc/bin-sm
tar xf input_simmedium.tar -C $PARSEC_APPS_PATH/facesim/inst/amd64-linux.gcc/bin-md
tar xf input_simlarge.tar -C $PARSEC_APPS_PATH/facesim/inst/amd64-linux.gcc/bin-lg
popd_silent
echo "DONE"

echo -n "Preparing raytrace..."
pushd_silent $PARSEC_APPS_PATH/raytrace/inputs
tar xf input_simsmall.tar
pushd_silent
echo "DONE"

echo -n "Preparing x264..."
pushd_silent $PARSEC_APPS_PATH/x264/inputs
tar xf input_simsmall.tar
tar xf input_simmedium.tar
tar xf input_simlarge.tar
pushd_silent
echo "DONE"

echo -n "Preparing vips..."
pushd_silent $PARSEC_APPS_PATH/vips/inputs
tar xf input_simsmall.tar
tar xf input_simmedium.tar
tar xf input_simlarge.tar
pushd_silent
echo "DONE"

echo -n "Preparing bodytrack..."
pushd_silent $PARSEC_APPS_PATH/bodytrack/inputs
tar xf input_simsmall.tar
tar xf input_simmedium.tar
tar xf input_simlarge.tar
pushd_silent
echo "DONE"

echo -n "Preparing ferret..."
pushd_silent $PARSEC_APPS_PATH/ferret/inputs
tar xf input_simsmall.tar
tar xf input_simmedium.tar
tar xf input_simlarge.tar
pushd_silent
echo "DONE"

echo -n "Preparing freqmine..."
pushd_silent $PARSEC_APPS_PATH/freqmine/inputs
tar xf input_simsmall.tar
tar xf input_simmedium.tar
tar xf input_simlarge.tar
pushd_silent
echo "DONE"


