CXX := g++
CXXFLAGS := -std=c++11 -Wall -Wconversion -Wextra
RM:= -rm -f

TARGET := main
OBJS := CGSolver.o COO2CSR.o main.o matvecops.o

$(TARGET): $(OBJS)
	$(CXX) -o $(TARGET) $(OBJS)

%.o: %.cpp
	$(CXX) -c -o $@ $< $(CXXFLAGS)

.PHONY: clean
clean:
	$(RM) $(OBJS) $(TARGET)