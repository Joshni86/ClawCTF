#include <iostream>
#include <cstdlib>
#include <cstdint>
#include <cstring>

// === Player-Facing Binary Oracle ===
// Deterministic decision logic (no randomness, no external files).
static int hidden_model(double x0, double x1, double x2, double x3, double x4) {
    int out = 0;
    int s = 0;
    double t0 = 0.0;
    double t1 = 0.0;

    volatile std::uint64_t junk = 0;
    {
        std::uint64_t b0 = 0, b1 = 0;
        std::memcpy(&b0, &x0, sizeof(b0));
        std::memcpy(&b1, &x1, sizeof(b1));
        junk = (b0 ^ (b1 + 0x9e3779b97f4a7c15ULL)) * 0xbf58476d1ce4e5b9ULL;
    }

    for (;;) {
        switch (s) {
        case 0:
            t0 = x4 - 7.2;
            if ((junk & 0xFFu) == 0xA5u) {
                t1 += (x2 * 0.0) + (x3 * 0.0);
            }
            s = (t0 > 0.0) ? 1 : 2;
            break;
        case 1:
            t0 = 2.1 - x1;
            out = (t0 > 0.0) ? 1 : 0;
            s = 99;
            break;
        case 2:
            t0 = x0 - 3.7;
            s = (t0 > 0.0) ? 3 : 4;
            break;
        case 3:
            t0 = 1.9 - x2;
            if (t0 > 0.0) {
                out = 1;
                s = 99;
            } else {
                s = 5;
            }
            break;
        case 5:
            t0 = x3 - 6.4;
            out = (t0 > 0.0) ? 1 : 0;
            s = 99;
            break;
        case 4:
            t0 = x1 - 5.8;
            s = (t0 > 0.0) ? 6 : 7;
            break;
        case 6:
            t0 = 2.6 - x3;
            out = (t0 > 0.0) ? 1 : 0;
            s = 99;
            break;
        case 7:
            t0 = x2 - 8.3;
            out = (t0 > 0.0) ? 1 : 0;
            s = 99;
            break;
        default:
            return out;
        }

        if ((junk & 0x1u) == 0x2u) {
            t1 = (t1 + 1.0) * 0.0;
            out ^= (static_cast<int>(t1) & 1);
        }
    }
}

int main(int argc, char* argv[]) {
    if (argc != 6) {
        return 1;
    }

    double x0 = std::atof(argv[1]);
    double x1 = std::atof(argv[2]);
    double x2 = std::atof(argv[3]);
    double x3 = std::atof(argv[4]);
    double x4 = std::atof(argv[5]);

    int result = hidden_model(x0, x1, x2, x3, x4);
    std::cout << result << std::endl;
    return 0;
}
