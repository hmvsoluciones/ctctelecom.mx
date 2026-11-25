# Calidad de los medios optimizados

Generado con `python tools/verificar_calidad.py --md docs/calidad-medios.md`.

SSIM compara el original con el archivo que sirve el sitio, a resolución de visualización (1440 px para video). **1.0 = idéntico**; por encima de 0.98 la diferencia no se aprecia a simple vista.

| archivo | tamaño | original | optimizado | SSIM | PSNR |
|---|---|---:|---:|---:|---:|
| 00-S-WAN-MPLS.png | 480x308 | 462 KB | 37 KB | 0.9974 | 50.3 dB |
| 00-S-WAN-MPLS.png | 960x615 | 462 KB | 90 KB | 0.9968 | 51.4 dB |
| 00-S-WAN-MPLS.png | 1022x655 | 462 KB | 72 KB | 0.9969 | 51.4 dB |
| Banner-web-3-poster.jpg | 480x272 | 91 KB | 21 KB | 0.9926 | 45.4 dB |
| Banner-web-3-poster.jpg | 960x544 | 91 KB | 52 KB | 0.9923 | 47.1 dB |
| Banner-web-3-poster.jpg | 1280x726 | 91 KB | 70 KB | 0.9927 | 47.9 dB |
| Ctc-Logo-2.png | 480x177 | 460 KB | 37 KB | 0.9997 | 53.4 dB |
| Ctc-Logo-2.png | 960x353 | 460 KB | 81 KB | 0.9992 | 54.6 dB |
| Ctc-Logo-2.png | 1600x589 | 460 KB | 143 KB | 0.9988 | 54.8 dB |
| Ctc-Logo-2.png | 1863x686 | 460 KB | 111 KB | 0.9986 | 55.1 dB |
| FONDOCTC.jpg | 480x214 | 448 KB | 24 KB | 0.9900 | 44.3 dB |
| FONDOCTC.jpg | 960x428 | 448 KB | 71 KB | 0.9888 | 44.9 dB |
| FONDOCTC.jpg | 1600x714 | 448 KB | 154 KB | 0.9855 | 44.8 dB |
| FONDOCTC.jpg | 2048x914 | 448 KB | 228 KB | 0.9840 | 44.8 dB |
| Imagen1ctc.png | 480x274 | 73 KB | 19 KB | 0.9989 | 49.5 dB |
| Imagen1ctc.png | 960x549 | 73 KB | 50 KB | 0.9981 | 49.8 dB |
| Imagen1ctc.png | 1050x600 | 73 KB | 58 KB | 0.9981 | 50.3 dB |
| ImagenLIZ2ctc.png | 480x600 | 502 KB | 46 KB | 0.9993 | 53.9 dB |
| ImagenLIZ2ctc.png | 960x1200 | 502 KB | 108 KB | 0.9991 | 54.7 dB |
| ImagenLIZ2ctc.png | 1080x1350 | 502 KB | 116 KB | 0.9991 | 54.9 dB |
| ImagenLIZ3ctc.png | 480x600 | 697 KB | 65 KB | 0.9996 | 53.1 dB |
| ImagenLIZ3ctc.png | 960x1200 | 697 KB | 157 KB | 0.9991 | 54.1 dB |
| ImagenLIZ3ctc.png | 1080x1350 | 697 KB | 168 KB | 0.9991 | 54.3 dB |
| ImagenLIZ4ctc.png | 480x600 | 566 KB | 38 KB | 0.9994 | 53.2 dB |
| ImagenLIZ4ctc.png | 960x1200 | 566 KB | 88 KB | 0.9989 | 53.9 dB |
| ImagenLIZ4ctc.png | 1080x1350 | 566 KB | 91 KB | 0.9989 | 53.9 dB |
| ImagenLIZ5ctc.png | 480x600 | 1116 KB | 85 KB | 0.9988 | 51.0 dB |
| ImagenLIZ5ctc.png | 960x1200 | 1116 KB | 186 KB | 0.9980 | 51.4 dB |
| ImagenLIZ5ctc.png | 1080x1350 | 1116 KB | 202 KB | 0.9979 | 51.5 dB |
| LAN-TO-LAN.png | 480x347 | 1086 KB | 29 KB | 0.9964 | 48.5 dB |
| LAN-TO-LAN.png | 960x695 | 1086 KB | 75 KB | 0.9940 | 48.6 dB |
| LAN-TO-LAN.png | 1216x880 | 1086 KB | 108 KB | 0.9931 | 48.7 dB |
| Marcadepago.png | 480x729 | 6558 KB | 87 KB | 0.9964 | 46.9 dB |
| Marcadepago.png | 960x1458 | 6558 KB | 266 KB | 0.9938 | 47.5 dB |
| Marcadepago.png | 1600x2431 | 6558 KB | 602 KB | 0.9906 | 47.0 dB |
| Marcadepago.png | 1664x2528 | 6558 KB | 670 KB | 0.9900 | 46.9 dB |
| TELECOM-FONDO-poster.jpg | 480x272 | 87 KB | 16 KB | 0.9860 | 45.3 dB |
| TELECOM-FONDO-poster.jpg | 960x544 | 87 KB | 48 KB | 0.9891 | 46.9 dB |
| TELECOM-FONDO-poster.jpg | 1280x726 | 87 KB | 68 KB | 0.9907 | 47.5 dB |
| TTT.jpg | 480x410 | 87 KB | 33 KB | 0.9973 | 46.0 dB |
| TTT.jpg | 930x794 | 87 KB | 77 KB | 0.9960 | 47.0 dB |
| acceso-a-ecosistemas-cloud.png | 480x458 | 871 KB | 26 KB | 0.9971 | 49.2 dB |
| acceso-a-ecosistemas-cloud.png | 960x916 | 871 KB | 68 KB | 0.9953 | 49.7 dB |
| acceso-a-ecosistemas-cloud.png | 1056x1008 | 871 KB | 79 KB | 0.9953 | 49.9 dB |
| backbone-red-propia.jpg | 480x402 | 104 KB | 21 KB | 0.9937 | 46.8 dB |
| backbone-red-propia.jpg | 940x788 | 104 KB | 61 KB | 0.9938 | 47.2 dB |
| carrier-interconexion-poster.jpg | 480x270 | 91 KB | 20 KB | 0.9948 | 46.7 dB |
| carrier-interconexion-poster.jpg | 960x540 | 91 KB | 47 KB | 0.9951 | 47.6 dB |
| carrier-interconexion-poster.jpg | 1280x720 | 91 KB | 66 KB | 0.9956 | 48.4 dB |
| celular-telefonia.png | 480x430 | 4599 KB | 34 KB | 0.9964 | 48.8 dB |
| celular-telefonia.png | 960x860 | 4599 KB | 87 KB | 0.9954 | 49.0 dB |
| celular-telefonia.png | 1600x1434 | 4599 KB | 192 KB | 0.9933 | 48.4 dB |
| celular-telefonia.png | 2048x1835 | 4599 KB | 288 KB | 0.9922 | 48.7 dB |
| cross-connects.jpg | 480x431 | 118 KB | 27 KB | 0.9972 | 47.0 dB |
| cross-connects.jpg | 960x862 | 118 KB | 72 KB | 0.9964 | 47.5 dB |
| cross-connects.jpg | 1024x919 | 118 KB | 80 KB | 0.9967 | 47.8 dB |
| ctc-imagen-24-estados.jpg | 480x402 | 147 KB | 62 KB | 0.9933 | 43.6 dB |
| ctc-imagen-24-estados.jpg | 940x788 | 147 KB | 176 KB | 0.9941 | 44.8 dB |
| data-center-connectivity-poster.jpg | 480x270 | 321 KB | 65 KB | 0.9967 | 42.7 dB |
| data-center-connectivity-poster.jpg | 960x540 | 321 KB | 203 KB | 0.9952 | 43.3 dB |
| data-center-connectivity-poster.jpg | 1280x720 | 321 KB | 290 KB | 0.9944 | 43.6 dB |
| datos-poster.jpg | 480x270 | 94 KB | 24 KB | 0.9928 | 45.6 dB |
| datos-poster.jpg | 960x540 | 94 KB | 56 KB | 0.9926 | 46.7 dB |
| datos-poster.jpg | 1280x720 | 94 KB | 77 KB | 0.9934 | 47.6 dB |
| favicon.png | 272x228 | 45 KB | 5 KB | 0.9973 | 49.3 dB |
| fortinet.png | 480x287 | 673 KB | 17 KB | 0.9950 | 47.9 dB |
| fortinet.png | 960x574 | 673 KB | 49 KB | 0.9917 | 48.4 dB |
| fortinet.png | 1040x622 | 673 KB | 59 KB | 0.9911 | 48.5 dB |
| huawei.jpg | 480x480 | 122 KB | 27 KB | 0.9957 | 46.6 dB |
| huawei.jpg | 960x960 | 122 KB | 69 KB | 0.9953 | 48.0 dB |
| huawei.jpg | 1024x1024 | 122 KB | 76 KB | 0.9955 | 48.3 dB |
| images (11).png | 318x159 | 3 KB | 4 KB | 0.9997 | 53.2 dB |
| internet-dedicado.png | 480x600 | 268 KB | 48 KB | 0.9993 | 51.3 dB |
| internet-dedicado.png | 960x1200 | 268 KB | 106 KB | 0.9995 | 54.0 dB |
| internet-dedicado.png | 1080x1350 | 268 KB | 96 KB | 0.9995 | 54.5 dB |
| internet-redundante.png | 480x480 | 6690 KB | 43 KB | 0.9922 | 46.1 dB |
| internet-redundante.png | 960x960 | 6690 KB | 139 KB | 0.9899 | 46.8 dB |
| internet-redundante.png | 1600x1600 | 6690 KB | 367 KB | 0.9866 | 46.5 dB |
| internet-redundante.png | 2048x2048 | 6690 KB | 639 KB | 0.9849 | 46.4 dB |
| mpls-imagen.jpeg | 480x292 | 115 KB | 19 KB | 0.9946 | 46.0 dB |
| mpls-imagen.jpeg | 960x585 | 115 KB | 46 KB | 0.9940 | 47.1 dB |
| mpls-imagen.jpeg | 1313x800 | 115 KB | 75 KB | 0.9942 | 47.8 dB |
| presencia-regional-america-latenia.jpg | 480x402 | 164 KB | 38 KB | 0.9876 | 44.5 dB |
| presencia-regional-america-latenia.jpg | 940x788 | 164 KB | 124 KB | 0.9885 | 44.9 dB |
| roaming-internacional.png | 480x540 | 6148 KB | 36 KB | 0.9936 | 47.7 dB |
| roaming-internacional.png | 960x1081 | 6148 KB | 100 KB | 0.9907 | 47.5 dB |
| roaming-internacional.png | 1600x1802 | 6148 KB | 239 KB | 0.9852 | 46.6 dB |
| roaming-internacional.png | 1952x2198 | 6148 KB | 364 KB | 0.9807 | 45.8 dB |
| servidoresdell-ibm.jpg | 480x320 | 101 KB | 11 KB | 0.9975 | 47.1 dB |
| servidoresdell-ibm.jpg | 960x640 | 101 KB | 28 KB | 0.9975 | 48.4 dB |
| servidoresdell-ibm.jpg | 1536x1024 | 101 KB | 53 KB | 0.9973 | 50.0 dB |
| sip-trunking-internacional.jpg | 480x417 | 189 KB | 35 KB | 0.9939 | 45.3 dB |
| sip-trunking-internacional.jpg | 960x834 | 189 KB | 86 KB | 0.9922 | 46.1 dB |
| sip-trunking-internacional.jpg | 1536x1335 | 189 KB | 155 KB | 0.9934 | 47.3 dB |
| sla-comprometidos.jpg | 480x402 | 103 KB | 26 KB | 0.9920 | 46.1 dB |
| sla-comprometidos.jpg | 940x788 | 103 KB | 60 KB | 0.9912 | 47.2 dB |
| soluciones-empresariales-poster.jpg | 480x270 | 185 KB | 44 KB | 0.9927 | 43.6 dB |
| soluciones-empresariales-poster.jpg | 960x540 | 185 KB | 109 KB | 0.9923 | 44.5 dB |
| soluciones-empresariales-poster.jpg | 1280x720 | 185 KB | 148 KB | 0.9924 | 45.4 dB |
| soporte2-poster.jpg | 480x270 | 76 KB | 20 KB | 0.9921 | 45.6 dB |
| soporte2-poster.jpg | 960x540 | 76 KB | 46 KB | 0.9912 | 46.9 dB |
| soporte2-poster.jpg | 1280x720 | 76 KB | 62 KB | 0.9918 | 47.9 dB |
| telefonia-integrada-con-crm-apis.png | 480x431 | 984 KB | 25 KB | 0.9967 | 48.7 dB |
| telefonia-integrada-con-crm-apis.png | 960x861 | 984 KB | 64 KB | 0.9942 | 49.2 dB |
| telefonia-integrada-con-crm-apis.png | 1088x976 | 984 KB | 78 KB | 0.9938 | 49.3 dB |
| telefonia-nube.png | 480x293 | 1652 KB | 23 KB | 0.9957 | 47.2 dB |
| telefonia-nube.png | 960x586 | 1652 KB | 61 KB | 0.9935 | 48.1 dB |
| telefonia-nube.png | 1536x937 | 1652 KB | 121 KB | 0.9920 | 48.6 dB |
| telefonia-poster.jpg | 480x270 | 84 KB | 22 KB | 0.9883 | 45.1 dB |
| telefonia-poster.jpg | 960x540 | 84 KB | 51 KB | 0.9889 | 46.4 dB |
| telefonia-poster.jpg | 1280x720 | 84 KB | 71 KB | 0.9907 | 47.2 dB |
| ucaas-unified-communications.png | 480x600 | 711 KB | 29 KB | 0.9986 | 49.8 dB |
| ucaas-unified-communications.png | 960x1200 | 711 KB | 74 KB | 0.9983 | 51.8 dB |
| ucaas-unified-communications.png | 1080x1350 | 711 KB | 87 KB | 0.9983 | 52.2 dB |
| Banner-web-3.mp4 | 1440px (vista) | 7777 KB | 3944 KB | 0.9921 | 47.3 dB |
| TELECOM-FONDO.mp4 | 1440px (vista) | 42173 KB | 19779 KB | 0.9920 | 46.2 dB |
| carrier-interconexion.mp4 | 1440px (vista) | 1202 KB | 765 KB | 0.9951 | 48.1 dB |
| data-center-connectivity.mp4 | 1440px (vista) | 7269 KB | 4845 KB | 0.9828 | 39.0 dB |
| datos.mp4 | 1440px (vista) | 1857 KB | 1251 KB | 0.9915 | 46.4 dB |
| soluciones-empresariales.mp4 | 1440px (vista) | 3399 KB | 2012 KB | 0.9851 | 43.0 dB |
| soporte2.mp4 | 1440px (vista) | 2067 KB | 1414 KB | 0.9920 | 48.3 dB |
| telefonia.mp4 | 1440px (vista) | 1574 KB | 1058 KB | 0.9899 | 46.8 dB |

- Imágenes: SSIM medio **0.9943**, mínimo 0.9807.
- Videos: SSIM medio **0.9901**, mínimo 0.9828.
