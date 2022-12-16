CXX := g++
CXXFLAGS := -O3 -std=c++11 -Wall -Wconversion -Wextra -Wpedantic
LIBFLAG :=  -ljpeg
RM := -rm -f

TARGET := main
OBJS := hw6.o image.o main.o

$(TARGET): $(OBJS)
	$(CXX) -o $(TARGET) $(OBJS) $(LIBFLAG)

%.o: %.cpp
	$(CXX) -c -o $@ $< $(CXXFLAGS)

.PHONY: run
run: $(TARGET)
	./$(TARGET)

.PHONY: clean
clean:
	$(RM) $(OBJS) $(TARGET)
	