(let ((x 10))
    (print x))

(let ((x 10) (y 20))
    (print (+ x y)))

(let ((x (+ 5 5))
      (y (* 4 5)))
    (print (+ x y)))

(let ((x 10))
    (let ((y 20))
        (print (+ x y))))

(defun square (x)
    (let ((result (* x x)))
        result))

(print (square 5))
