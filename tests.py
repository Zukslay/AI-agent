from functions.write_file import write_file

def main():
    
    inputs = [["lorem.txt", "wait, this isn't lorem ipsum"],
               ["pkg/morelorem.txt", "lorem ipsum dolor sit amet"],
                 ["/tmp/temp.txt","this should not be allowed"]]
    
    for input in inputs:
        result = write_file("calculator", input[0], input[1])
        input[0] = "current directory" if input[0] == "." else input[0]
        print(f"Result for '{input[0]}' directory:")
        print(result)




if __name__ == "__main__":
    main()