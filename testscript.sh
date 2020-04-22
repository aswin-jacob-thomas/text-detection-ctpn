#!/bin/bash 
for f in *jp*g; do {
# local filename = $f;
echo $f;
printf "\n"
echo '--------------------------------------------------------------------------'
curl -k -F 'file=@/home/aswin/Documents/reciept-detection/text-detection-ctpn/'${f} -v localhost:8080/detect ; 
printf "\n"
echo '--------------------------------------------------------------------------'

}
done