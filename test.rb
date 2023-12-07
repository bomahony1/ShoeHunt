def fib2(arr)
    if arr.length == 12
        return arr
    else
        arr << arr[-1] + arr[-2]
        fib(arr)
    end
end

def fib1(arr)
    (1..10).each do |i|
        arr << arr[-1] + arr[-2]
    end
    return arr
end

puts fib_it([0, 1])