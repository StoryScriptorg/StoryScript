from timeit import timeit
from processor import execute


def benchmark():
    print("Benchmarking started...")
    with open("benchmark.txt", "w") as f:
        hello_world = 'print ("Hello world!")'
        var_a = "var a = 10"
        var_b = "var b = 3.14"
        var_c = 'var c = "String"'
        hello_loop = 'loopfor 10 print ("Hello world!") end'
        tingtong_loop = 'loopfor 10 print ("ting") && print("tong") end'
        f.write(
            f"Hello world (Once): {timeit(lambda: execute(hello_world), number=1)}ms\n"
        )
        f.write(
            f"Hello world (Once): {timeit(lambda: execute(hello_world), number=1)}ms\n"
        )
        f.write(
            f"Hello world (Once): {timeit(lambda: execute(hello_world), number=1)}ms\n"
        )
        f.write(
            f"Hello world (25): {timeit(lambda: execute(hello_world), number=25)}ms\n"
        )
        f.write(
            f"Hello world (50): {timeit(lambda: execute(hello_world), number=50)}ms\n"
        )
        f.write(
            f"Variable declaration (Once): {timeit(lambda: execute(var_a), number=1)}ms\n"
        )
        f.write(
            f"Variable declaration (Once): {timeit(lambda: execute(var_b), number=1)}ms\n"
        )
        f.write(
            f"Variable declaration (Once): {timeit(lambda: execute(var_c), number=1)}ms\n"
        )
        f.write(
            f"Hello world loopfor (10) loop (Once): {timeit(lambda: execute(hello_loop), number=1)}ms\n"
        )
        f.write(
            f"Hello world loopfor (10) loop (Once): {timeit(lambda: execute(hello_loop), number=1)}ms\n"
        )
        f.write(
            f"tingtong loopfor (10) loop (Once): {timeit(lambda: execute(tingtong_loop), number=1)}ms\n"
        )
        f.write(
            f"tingtong loopfor (10) loop (Once): {timeit(lambda: execute(tingtong_loop), number=1)}ms\n"
        )


benchmark()
