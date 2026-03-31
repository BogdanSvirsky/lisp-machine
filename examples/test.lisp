(defmacro my-when (condition &body body)
  `(if ,condition
       (progn ,@body)))

(let ((x 10)
      (y 5))
  (my-when (> x y)
    (print "Executing body")
    (print "Executing body")
    (print "Executing body")
    (print "Executing body")
    (print "Executing body")
    (print "Executing body")
    (print "Executing body")
    (print (+ x y))))

