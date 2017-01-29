## ~20000 samples:

### Categorization
mult_nb:        0.718059
mult_nb_tfidf:  0.461945
bern_nb:        0.586969
bern_nb_tfidf:  0.586969
svc:            0.586969
svc_tfidf:      0.767951
rf:             0.713363
rf_tfidf:       0.709255

                400 dimentional (9.37 GB)       200 dimensional (4.9GB)

argmax(LL):     0.7091796875                     0.7201171875
word2doc:       0.679123459206                   0.681080023479
CNN:            -                                -

### Clustering:
MiniBatchKMeans:
	homogenity:	  0.233553017635                   0.236841050147
	completeness:	0.226445794028                   0.249476009557
	v-measure:	  0.22994450066                    0.242994395985

AffinityPropagation:
	homogenity:	  0.791271760203                   0.652669953895
	completeness:	0.201767501168                   0.190574928079
	v-measure:	  0.321544035591                   0.295009272351

MeanShift:
	homogenity:	 -2.79616603853e-16               -2.79616603853e-16
	completeness:	1.0                              1.0
	v-measure:	 -5.59233207705e-16               -5.59233207705e-16

SpectralClustering:
	homogenity:	  0.00926710375476                 0.00789771144523
	completeness:	0.115924832081                   0.130907002339
	v-measure:	  0.017162246745                   0.0148966948232

Ward:
	homogenity:	  0.259648022342                   0.26562522413
	completeness:	0.268177584554                   0.268206528374
	v-measure:	  0.26384388539                    0.266909635398

AgglomerativeClustering:
	homogenity:	  0.0106941242306                  0.0106941242306
	completeness:	0.341135629001                   0.341135629001
	v-measure:	  0.0207381369114                  0.0207381369114

DBSCAN:
	homogenity:	  0.0451934853679                  0.0451934853679
	completeness:	0.159479197566                   0.159479197566
	v-measure:	  0.0704287516866                  0.0704287516866

Birch:
	homogenity:	  0.256166859527                   0.279111972684
	completeness:	0.248528220592                   0.266110719439
	v-measure:	  0.252289734062                   0.272456333634

## ~40000 samples:
### Categorization
mult_nb         0.732004
mult_nb_tfidf   0.492396
bern_nb         0.625887
bern_nb_tfidf   0.625887
svc             0.743156
svc_tfidf       0.784049
rf              0.720514
rf_tfidf        0.718824

                200 dimensional (4.9GB)
argmax(LL):     0.79810938555
word2doc:       0.701926326462
CNN:            -
