(defun factorial (n acc)
    (if (== n 1)
        acc
        (factorial (- n 1) (* n acc))))

(defun fact (n)
    (factorial n 1))

(print (fact 5))

(defun sum (n acc)
    (if (== n 0)
        acc
        (sum (- n 1) (+ n acc))))

(defun s (n)
    (sum n 0))

(print (s 10))

(defun fib (n a b)
    (if (> n 0)
        (fib (- n 1) b (+ a b))
        a
    )
)

(defun fb (n)
    (fib n 0 1))

(print (fb 10))