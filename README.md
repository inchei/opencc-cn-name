# opencc-cn-name

[![npm version](https://img.shields.io/npm/v/opencc-cn-name?style=flat-square&label=npm)](https://www.npmjs.com/package/opencc-cn-name)
[![PyPI version](https://img.shields.io/pypi/v/opencc-cn-name?style=flat-square&label=PyPI)](https://pypi.org/project/opencc-cn-name/)

[OpenCC](https://github.com/BYVoid/OpenCC) 的补充库：处理 OpenCC 无法正确转换的日本人名用字，将日文人名转为简体中文。

Python / JavaScript 两端同源，单一权威数据源 `data/name_cn.json`，由
`scripts/gen.py` 生成各语言数据文件，CI 校验一致。

## 安装

```bash
pip install opencc-cn-name opencc        # Python
npm install opencc-cn-name opencc-js     # JS
```

## 使用

### Python

```python
import opencc
from opencc_cn_name import refined_to_cn

converters = (
    opencc.OpenCC("jp2t"), opencc.OpenCC("t2s"),
    opencc.OpenCC("tw2s"), opencc.OpenCC("hk2s"), opencc.OpenCC("t2jp"),
)
refined_to_cn("高橋耕次郎", converters)  # 高桥耕次郎
refined_to_cn("高橋耕次郎")              # 也可不传，内部自动用 opencc
```

### JavaScript

```js
import { OpenCC } from 'opencc-js';
import { refinedToCN } from 'opencc-cn-name';

const converters = {
  jp2t: OpenCC.Converter({ from: 'jp', to: 'tw' }),
  t2s:  OpenCC.Converter({ from: 'tw', to: 'cn' }),
  tw2s: OpenCC.Converter({ from: 'tw', to: 'cn' }),
  hk2s: OpenCC.Converter({ from: 'hk', to: 'cn' }),
  t2jp: OpenCC.Converter({ from: 'tw', to: 'jp' }),
};
refinedToCN('高橋耕次郎', converters); // 高桥耕次郎
```

## CDN（浏览器 / userscript）

```html
<script src="https://cdn.jsdelivr.net/npm/opencc-js@1.0.5/dist/umd/full.js"></script>
<script src="https://cdn.jsdelivr.net/npm/opencc-cn-name/dist/umd/opencc-cn-name.js"></script>
<script>
  openccCN.refinedToCN('澁谷', { /* 同上 5 个 converter */ }); // 涩谷
</script>
```

Tampermonkey 用 `// @require <上述 jsDelivr 链接>`。

## 开发

```bash
python3 scripts/gen.py            # 校验生成文件与 name_cn.json 一致（--write 则重新生成）
cd python && uv run --with opencc --with pytest python -m pytest   # Python 测试
cd js && npm install && npm run build && node --test               # JS 测试 + 构建
```

改数据只编辑 `data/name_cn.json`，再 `scripts/gen.py --write` 同步两端。

## License

GPL-3.0-only