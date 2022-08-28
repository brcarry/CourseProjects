.ORIG x3000

START   .BLKW #1
        .BLKW #1
L1      .BLKW #3
L2      .BLKW #1
L3      .STRINGZ "1234"
L4      .FILL xFFFF

.END


.ORIG x3000

L3      .STRINGZ "1234"

.END