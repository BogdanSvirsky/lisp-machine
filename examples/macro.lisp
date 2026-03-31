(defmacro twice (x)
    `(* ,x 2))

(print (twice 5))

(defmacro swap (a b)
    `(+ ,a ,b))

(print (swap 10 20))

(print "done")

(defmacro myif (cond first second) 
    `(if ,cond ,first ,second))


(myif 5
    (print "Then")
    (print "Else"))
