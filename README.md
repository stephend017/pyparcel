# pyparcel

pyparcel is a Python library to easily perform conversions between Python values and C structs represesented as Python [`bytes`](https://docs.python.org/3/library/stdtypes.html#bytes) objects. pyparcel extends the usage of [`struct`](https://docs.python.org/3/library/struct.html) and provides a simpler way to pack classes.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

```bash
pip install pyparcel
```

## Usage

```python
import pyparcel

foo: Foo = Foo(8, 5.7, "Hello World") # Foo(int, float, str)
data: bytes = pyparcel.pack(foo) # b'\x08\x00\x00\x00ff\xb6@\x0b\x00\x00\x00Hello World'

# ...

bar: Foo = Foo()
pyparcel.unpack(data, bar) # foo == bar
# or
baz: Foo = pyparcel.unpack(data, Foo()) # foo == baz

```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)