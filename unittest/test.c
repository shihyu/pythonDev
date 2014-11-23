#include <stdlib.h>
#include "test.h"

int area(rect s) {
    return abs(s.a.x - s.b.x) * abs(s.a.y - s.b.y);
}
