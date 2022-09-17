from nanoid import generate


class NanoidTool:
    @classmethod
    def rng2generate(cls, rng, options=None):
        generate()

    """
    static rng2generator(
    rng:() => number,
    options?:{
      alphabet?: string,
      size?: number,
    }
  ): (() => string){
    const cls = NanoidTool;

    const alphabet = options?.alphabet ?? urlAlphabet;
    const size = options?.size ?? cls.Default.size();

    const generator = customRandom(
      alphabet,
      size,
      size => (new Uint8Array(size)).map(() => 256 * rng()),
    );
    return generator;
  }
    """