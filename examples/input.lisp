(defun process_input ()
    (let ((x (read)))
        (print (* x 2))))

(process_input)

(defun print_list ()
    (let ((lst (read)))
        (print lst)
    )
)

(print_list)

(print (+ (read) 10))

(defun sum_input ()
    (let ((x (read)))
        (if (null? x)
            0
            (+ x (sum_input)))))

(print (sum_input))