class RawProvider {
public:
    RawProvider(const unsigned char *buffer);
    ~RawProvider();
    unsigned char getByte(void);
private:
    const unsigned char *buff;
    int index;
};

class RLEProvider {
public:
    RLEProvider(const unsigned char *buffer);
    ~RLEProvider();
    unsigned char getByte(void);
private:
    const unsigned char *buff;
    int index;
    unsigned char pair;
    bool is_zero;
    int bitcount;
};
