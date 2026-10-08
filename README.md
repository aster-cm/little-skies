# little-skies ✦

A tiny, dependency-free Python script that makes a repeatable night sky from any word or phrase. The same seed always gives the same SVG; change a letter and the stars rearrange.

```sh
python3 sky.py "first light" --out first-light.svg
python3 sky.py "aster" --width 1200 --height 450 --out aster.svg
python3 -m unittest -v
```

Open the SVG in a browser, or use it as a background in something else. The generated sky is yours to use; the source is MIT-licensed.

This started as a small experiment in making a personal, reproducible sky rather than another dashboard.
