CXX := g++
CXXFLAGS := -O3 -std=c++11 -Wall -Wconversion -Wextra
RM:= -rm -f

TARGET := main
OBJS := CGSolver.o COO2CSR.o heat.o main.o matvecops.o sparse.o

$(TARGET): $(OBJS)
	$(CXX) -o $(TARGET) $(OBJS)

%.o: %.cpp
	$(CXX) -c -o $@ $< $(CXXFLAGS)

.PHONY: clean
clean:
	$(RM) $(OBJS) $(TARGET)