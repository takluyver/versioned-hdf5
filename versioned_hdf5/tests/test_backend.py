import numpy as np
from numpy.testing import assert_equal

from ndindex import Slice, Tuple

from pytest import raises, xfail

import itertools

from .helpers import setup
from ..backend import (create_base_dataset, write_dataset,
                       create_virtual_dataset, DEFAULT_CHUNK_SIZE,
                       write_dataset_chunks)

CHUNK_SIZE_3D = 2**4 # = cbrt(DEFAULT_CHUNK_SIZE)

def test_initialize():
    with setup():
        pass

def test_create_base_dataset():
    with setup() as f:
        create_base_dataset(f, 'test_data', data=np.ones((DEFAULT_CHUNK_SIZE,)))
        assert f['_version_data/test_data/raw_data'].dtype == np.float64

def test_write_dataset():
    with setup() as f:
        slices1 = write_dataset(f, 'test_data', np.ones((2*DEFAULT_CHUNK_SIZE,)))
        slices2 = write_dataset(f, 'test_data',
                                np.concatenate((2*np.ones((DEFAULT_CHUNK_SIZE,)),
                                                2*np.ones((DEFAULT_CHUNK_SIZE,)),
                                                3*np.ones((DEFAULT_CHUNK_SIZE,)),
                                )))

        assert slices1 == {
            (Slice(0*DEFAULT_CHUNK_SIZE, 1*DEFAULT_CHUNK_SIZE),):
                slice(0*DEFAULT_CHUNK_SIZE, 1*DEFAULT_CHUNK_SIZE),
            (Slice(1*DEFAULT_CHUNK_SIZE, 2*DEFAULT_CHUNK_SIZE),):
                slice(0*DEFAULT_CHUNK_SIZE, 1*DEFAULT_CHUNK_SIZE)}
        assert slices2 == {
            (Slice(0*DEFAULT_CHUNK_SIZE, 1*DEFAULT_CHUNK_SIZE),):
                slice(1*DEFAULT_CHUNK_SIZE, 2*DEFAULT_CHUNK_SIZE),
            (Slice(1*DEFAULT_CHUNK_SIZE, 2*DEFAULT_CHUNK_SIZE),):
                slice(1*DEFAULT_CHUNK_SIZE, 2*DEFAULT_CHUNK_SIZE),
            (Slice(2*DEFAULT_CHUNK_SIZE, 3*DEFAULT_CHUNK_SIZE),):
                slice(2*DEFAULT_CHUNK_SIZE, 3*DEFAULT_CHUNK_SIZE)}

        ds = f['/_version_data/test_data/raw_data']
        assert ds.shape == (3*DEFAULT_CHUNK_SIZE,)
        assert_equal(ds[0:1*DEFAULT_CHUNK_SIZE], 1.0)
        assert_equal(ds[1*DEFAULT_CHUNK_SIZE:2*DEFAULT_CHUNK_SIZE], 2.0)
        assert_equal(ds[2*DEFAULT_CHUNK_SIZE:3*DEFAULT_CHUNK_SIZE], 3.0)
        assert_equal(ds[3*DEFAULT_CHUNK_SIZE:4*DEFAULT_CHUNK_SIZE], 0.0)
        assert ds.dtype == np.float64

def test_write_dataset_multidimension():
    with setup() as f:
        chunks = 3*(CHUNK_SIZE_3D,)
        data = np.zeros((2*CHUNK_SIZE_3D, 2*CHUNK_SIZE_3D, 2*CHUNK_SIZE_3D))
        slices1 = write_dataset(f, 'test_data', data, chunks=chunks)
        data2 = data.copy()
        for n, (i, j, k) in enumerate(itertools.product([0, 1], repeat=3)):
            data2[i*CHUNK_SIZE_3D:(i+1)*CHUNK_SIZE_3D,
                  j*CHUNK_SIZE_3D:(j+1)*CHUNK_SIZE_3D,
                  k*CHUNK_SIZE_3D:(k+1)*CHUNK_SIZE_3D] = n

        slices2 = write_dataset(f, 'test_data', data2, chunks=chunks)


        assert slices1 == {
            (Slice(0*CHUNK_SIZE_3D, 1*CHUNK_SIZE_3D),
             Slice(0*CHUNK_SIZE_3D, 1*CHUNK_SIZE_3D),
             Slice(0*CHUNK_SIZE_3D, 1*CHUNK_SIZE_3D),
             ): slice(0*CHUNK_SIZE_3D, 1*CHUNK_SIZE_3D),
            (Slice(0*CHUNK_SIZE_3D, 1*CHUNK_SIZE_3D),
             Slice(0*CHUNK_SIZE_3D, 1*CHUNK_SIZE_3D),
             Slice(1*CHUNK_SIZE_3D, 2*CHUNK_SIZE_3D),
             ): slice(0*CHUNK_SIZE_3D, 1*CHUNK_SIZE_3D),
            (Slice(0*CHUNK_SIZE_3D, 1*CHUNK_SIZE_3D),
             Slice(1*CHUNK_SIZE_3D, 2*CHUNK_SIZE_3D),
             Slice(0*CHUNK_SIZE_3D, 1*CHUNK_SIZE_3D),
             ): slice(0*CHUNK_SIZE_3D, 1*CHUNK_SIZE_3D),
            (Slice(0*CHUNK_SIZE_3D, 1*CHUNK_SIZE_3D),
             Slice(1*CHUNK_SIZE_3D, 2*CHUNK_SIZE_3D),
             Slice(1*CHUNK_SIZE_3D, 2*CHUNK_SIZE_3D),
             ): slice(0*CHUNK_SIZE_3D, 1*CHUNK_SIZE_3D),
            (Slice(1*CHUNK_SIZE_3D, 2*CHUNK_SIZE_3D),
             Slice(0*CHUNK_SIZE_3D, 1*CHUNK_SIZE_3D),
             Slice(0*CHUNK_SIZE_3D, 1*CHUNK_SIZE_3D),
             ): slice(0*CHUNK_SIZE_3D, 1*CHUNK_SIZE_3D),
            (Slice(1*CHUNK_SIZE_3D, 2*CHUNK_SIZE_3D),
             Slice(0*CHUNK_SIZE_3D, 1*CHUNK_SIZE_3D),
             Slice(1*CHUNK_SIZE_3D, 2*CHUNK_SIZE_3D),
             ): slice(0*CHUNK_SIZE_3D, 1*CHUNK_SIZE_3D),
            (Slice(1*CHUNK_SIZE_3D, 2*CHUNK_SIZE_3D),
             Slice(1*CHUNK_SIZE_3D, 2*CHUNK_SIZE_3D),
             Slice(0*CHUNK_SIZE_3D, 1*CHUNK_SIZE_3D),
             ): slice(0*CHUNK_SIZE_3D, 1*CHUNK_SIZE_3D),
            (Slice(1*CHUNK_SIZE_3D, 2*CHUNK_SIZE_3D),
             Slice(1*CHUNK_SIZE_3D, 2*CHUNK_SIZE_3D),
             Slice(1*CHUNK_SIZE_3D, 2*CHUNK_SIZE_3D),
             ): slice(0*CHUNK_SIZE_3D, 1*CHUNK_SIZE_3D),
        }
        assert slices2 == {
            (Slice(0*CHUNK_SIZE_3D, 1*CHUNK_SIZE_3D),
             Slice(0*CHUNK_SIZE_3D, 1*CHUNK_SIZE_3D),
             Slice(0*CHUNK_SIZE_3D, 1*CHUNK_SIZE_3D),
             ): slice(0*CHUNK_SIZE_3D, 1*CHUNK_SIZE_3D),
            (Slice(0*CHUNK_SIZE_3D, 1*CHUNK_SIZE_3D),
             Slice(0*CHUNK_SIZE_3D, 1*CHUNK_SIZE_3D),
             Slice(1*CHUNK_SIZE_3D, 2*CHUNK_SIZE_3D),
             ): slice(1*CHUNK_SIZE_3D, 2*CHUNK_SIZE_3D),
            (Slice(0*CHUNK_SIZE_3D, 1*CHUNK_SIZE_3D),
             Slice(1*CHUNK_SIZE_3D, 2*CHUNK_SIZE_3D),
             Slice(0*CHUNK_SIZE_3D, 1*CHUNK_SIZE_3D),
             ): slice(2*CHUNK_SIZE_3D, 3*CHUNK_SIZE_3D),
            (Slice(0*CHUNK_SIZE_3D, 1*CHUNK_SIZE_3D),
             Slice(1*CHUNK_SIZE_3D, 2*CHUNK_SIZE_3D),
             Slice(1*CHUNK_SIZE_3D, 2*CHUNK_SIZE_3D),
             ): slice(3*CHUNK_SIZE_3D, 4*CHUNK_SIZE_3D),
            (Slice(1*CHUNK_SIZE_3D, 2*CHUNK_SIZE_3D),
             Slice(0*CHUNK_SIZE_3D, 1*CHUNK_SIZE_3D),
             Slice(0*CHUNK_SIZE_3D, 1*CHUNK_SIZE_3D),
             ): slice(4*CHUNK_SIZE_3D, 5*CHUNK_SIZE_3D),
            (Slice(1*CHUNK_SIZE_3D, 2*CHUNK_SIZE_3D),
             Slice(0*CHUNK_SIZE_3D, 1*CHUNK_SIZE_3D),
             Slice(1*CHUNK_SIZE_3D, 2*CHUNK_SIZE_3D),
             ): slice(5*CHUNK_SIZE_3D, 6*CHUNK_SIZE_3D),
            (Slice(1*CHUNK_SIZE_3D, 2*CHUNK_SIZE_3D),
             Slice(1*CHUNK_SIZE_3D, 2*CHUNK_SIZE_3D),
             Slice(0*CHUNK_SIZE_3D, 1*CHUNK_SIZE_3D),
             ): slice(6*CHUNK_SIZE_3D, 7*CHUNK_SIZE_3D),
            (Slice(1*CHUNK_SIZE_3D, 2*CHUNK_SIZE_3D),
             Slice(1*CHUNK_SIZE_3D, 2*CHUNK_SIZE_3D),
             Slice(1*CHUNK_SIZE_3D, 2*CHUNK_SIZE_3D),
             ): slice(7*CHUNK_SIZE_3D, 8*CHUNK_SIZE_3D),
        }

        ds = f['/_version_data/test_data/raw_data']
        assert ds.shape == (8*CHUNK_SIZE_3D, CHUNK_SIZE_3D, CHUNK_SIZE_3D)
        for n in range(8):
            assert_equal(ds[n*CHUNK_SIZE_3D:(n+1)*CHUNK_SIZE_3D], n)
        assert ds.dtype == np.float64

def test_write_dataset_chunks():
    with setup() as f:
        slices1 = write_dataset(f, 'test_data', np.ones((2*DEFAULT_CHUNK_SIZE,)))
        slices2 = write_dataset_chunks(f, 'test_data',
                                       {0: slices1[0],
                                        1: 2*np.ones((DEFAULT_CHUNK_SIZE,)),
                                        2: 2*np.ones((DEFAULT_CHUNK_SIZE,)),
                                        3: 3*np.ones((DEFAULT_CHUNK_SIZE,)),
                                       })

        assert slices1 == [slice(0*DEFAULT_CHUNK_SIZE, 1*DEFAULT_CHUNK_SIZE),
                           slice(0*DEFAULT_CHUNK_SIZE, 1*DEFAULT_CHUNK_SIZE)]
        assert slices2 == [slice(0*DEFAULT_CHUNK_SIZE, 1*DEFAULT_CHUNK_SIZE),
                           slice(1*DEFAULT_CHUNK_SIZE, 2*DEFAULT_CHUNK_SIZE),
                           slice(1*DEFAULT_CHUNK_SIZE, 2*DEFAULT_CHUNK_SIZE),
                           slice(2*DEFAULT_CHUNK_SIZE, 3*DEFAULT_CHUNK_SIZE)]

        ds = f['/_version_data/test_data/raw_data']
        assert ds.shape == (3*DEFAULT_CHUNK_SIZE,)
        assert_equal(ds[0:1*DEFAULT_CHUNK_SIZE], 1.0)
        assert_equal(ds[1*DEFAULT_CHUNK_SIZE:2*DEFAULT_CHUNK_SIZE], 2.0)
        assert_equal(ds[2*DEFAULT_CHUNK_SIZE:3*DEFAULT_CHUNK_SIZE], 3.0)
        assert_equal(ds[3*DEFAULT_CHUNK_SIZE:4*DEFAULT_CHUNK_SIZE], 0.0)
        assert ds.dtype == np.float64

def test_write_dataset_chunks_multidimension():
    with setup() as f:
        chunks = 3*(CHUNK_SIZE_3D,)
        data = np.zeros((2*CHUNK_SIZE_3D, 2*CHUNK_SIZE_3D, 2*CHUNK_SIZE_3D))
        slices1 = write_dataset(f, 'test_data', data, chunks=chunks)
        data_dict = {}
        for n, (i, j, k) in enumerate(itertools.product([0, 1], repeat=3)):
            data_dict[n] = n*np.ones(chunks)
        data_dict[0] = slices1[0]

        slices1 = write_dataset(f, 'test_data', data, chunks=chunks)
        slices2 = write_dataset_chunks(f, 'test_data', data_dict)


        assert slices1 == 8*[slice(0*CHUNK_SIZE_3D, 1*CHUNK_SIZE_3D)]
        assert slices2 == [slice(i*CHUNK_SIZE_3D, (i+1)*CHUNK_SIZE_3D) for i
                           in range(8)]

        ds = f['/_version_data/test_data/raw_data']
        assert ds.shape == (8*CHUNK_SIZE_3D, CHUNK_SIZE_3D, CHUNK_SIZE_3D)
        for n in range(8):
            assert_equal(ds[n*CHUNK_SIZE_3D:(n+1)*CHUNK_SIZE_3D], n)
        assert ds.dtype == np.float64


def test_write_dataset_offset():
    with setup() as f:
        slices1 = write_dataset(f, 'test_data', np.ones((2*DEFAULT_CHUNK_SIZE,)))
        slices2 = write_dataset(f, 'test_data',
                                np.concatenate((2*np.ones((DEFAULT_CHUNK_SIZE,)),
                                                2*np.ones((DEFAULT_CHUNK_SIZE,)),
                                                3*np.ones((DEFAULT_CHUNK_SIZE - 2,)))))

        assert slices1 == {
            (Slice(0*DEFAULT_CHUNK_SIZE, 1*DEFAULT_CHUNK_SIZE),):
                slice(0*DEFAULT_CHUNK_SIZE, 1*DEFAULT_CHUNK_SIZE),
            (Slice(1*DEFAULT_CHUNK_SIZE, 2*DEFAULT_CHUNK_SIZE),):
                slice(0*DEFAULT_CHUNK_SIZE, 1*DEFAULT_CHUNK_SIZE)}
        assert slices2 == {
            (Slice(0*DEFAULT_CHUNK_SIZE, 1*DEFAULT_CHUNK_SIZE),):
                slice(1*DEFAULT_CHUNK_SIZE, 2*DEFAULT_CHUNK_SIZE),
            (Slice(1*DEFAULT_CHUNK_SIZE, 2*DEFAULT_CHUNK_SIZE),):
                slice(1*DEFAULT_CHUNK_SIZE, 2*DEFAULT_CHUNK_SIZE),
            (Slice(2*DEFAULT_CHUNK_SIZE, 3*DEFAULT_CHUNK_SIZE - 2),):
                slice(2*DEFAULT_CHUNK_SIZE, 3*DEFAULT_CHUNK_SIZE - 2)}

        ds = f['/_version_data/test_data/raw_data']
        assert ds.shape == (3*DEFAULT_CHUNK_SIZE,)
        assert_equal(ds[0*DEFAULT_CHUNK_SIZE:1*DEFAULT_CHUNK_SIZE], 1.0)
        assert_equal(ds[1*DEFAULT_CHUNK_SIZE:2*DEFAULT_CHUNK_SIZE], 2.0)
        assert_equal(ds[2*DEFAULT_CHUNK_SIZE:3*DEFAULT_CHUNK_SIZE - 2], 3.0)
        assert_equal(ds[3*DEFAULT_CHUNK_SIZE-2:4*DEFAULT_CHUNK_SIZE], 0.0)


def test_write_dataset_offset_multidimension():
    xfail()
    # TODO: Fix this test once this is implemented
    with setup() as f:
        chunks = 3*(CHUNK_SIZE_3D,)
        data = np.zeros((2*CHUNK_SIZE_3D, 2*CHUNK_SIZE_3D, 2*CHUNK_SIZE_3D))
        slices1 = write_dataset(f, 'test_data', data, chunks=chunks)
        data2 = np.empty((2*CHUNK_SIZE_3D - 2, 2*CHUNK_SIZE_3D - 2,
                          2*CHUNK_SIZE_3D - 2))
        for n, (i, j, k) in enumerate(itertools.product([0, 1], repeat=3)):
            data2[i*CHUNK_SIZE_3D:(i+1)*CHUNK_SIZE_3D,
                  j*CHUNK_SIZE_3D:(j+1)*CHUNK_SIZE_3D,
                  k*CHUNK_SIZE_3D:(k+1)*CHUNK_SIZE_3D] = n

        slices2 = write_dataset(f, 'test_data', data2, chunks=chunks)

        assert slices1 == 8*[slice(0*CHUNK_SIZE_3D, 1*CHUNK_SIZE_3D)]
        assert slices2 == [slice(i*CHUNK_SIZE_3D, (i+1)*CHUNK_SIZE_3D) for i
                           in range(8)]

        ds = f['/_version_data/test_data/raw_data']
        assert ds.shape == (8*CHUNK_SIZE_3D, CHUNK_SIZE_3D - 2, CHUNK_SIZE_3D - 2)
        for n in range(8):
            assert_equal(ds[n*CHUNK_SIZE_3D:(n+1)*CHUNK_SIZE_3D], n)
        assert ds.dtype == np.float64

def test_create_virtual_dataset():
    with setup(version_name='test_version') as f:
        slices1 = write_dataset(f, 'test_data', np.ones((2*DEFAULT_CHUNK_SIZE,)))
        slices2 = write_dataset(f, 'test_data',
                                np.concatenate((2*np.ones((DEFAULT_CHUNK_SIZE,)),
                                                3*np.ones((DEFAULT_CHUNK_SIZE,)))))

        virtual_data = create_virtual_dataset(f, 'test_version', 'test_data',
            {**slices1,
             Tuple(Slice(2*DEFAULT_CHUNK_SIZE, 3*DEFAULT_CHUNK_SIZE),):
             slices2[(Slice(1*DEFAULT_CHUNK_SIZE, 2*DEFAULT_CHUNK_SIZE),)]})

        assert virtual_data.shape == (3*DEFAULT_CHUNK_SIZE,)
        assert_equal(virtual_data[0:2*DEFAULT_CHUNK_SIZE], 1.0)
        assert_equal(virtual_data[2*DEFAULT_CHUNK_SIZE:3*DEFAULT_CHUNK_SIZE], 3.0)
        assert virtual_data.dtype == np.float64


def test_create_virtual_dataset_multidimension():
    with setup(version_name=['test_version1', 'test_version2']) as f:
        chunks = 3*(CHUNK_SIZE_3D,)
        shape = (2*CHUNK_SIZE_3D, 2*CHUNK_SIZE_3D, 2*CHUNK_SIZE_3D)
        data = np.ones(shape)
        slices1 = write_dataset(f, 'test_data', data, chunks=chunks)

        virtual_data = create_virtual_dataset(f, 'test_version1', 'test_data', slices1)

        assert virtual_data.shape == shape
        assert_equal(virtual_data[:], 1)
        assert virtual_data.dtype == np.float64

        data2 = data.copy()
        for n, (i, j, k) in enumerate(itertools.product([0, 1], repeat=3)):
            data2[i*CHUNK_SIZE_3D:(i+1)*CHUNK_SIZE_3D,
                  j*CHUNK_SIZE_3D:(j+1)*CHUNK_SIZE_3D,
                  k*CHUNK_SIZE_3D:(k+1)*CHUNK_SIZE_3D] = n

        slices2 = write_dataset(f, 'test_data', data2, chunks=chunks)

        virtual_data2 = create_virtual_dataset(f, 'test_version2', 'test_data', slices2)

        assert virtual_data2.shape == shape
        for n, (i, j, k) in enumerate(itertools.product([0, 1], repeat=3)):
            assert_equal(virtual_data2[i*CHUNK_SIZE_3D:(i+1)*CHUNK_SIZE_3D,
                  j*CHUNK_SIZE_3D:(j+1)*CHUNK_SIZE_3D,
                  k*CHUNK_SIZE_3D:(k+1)*CHUNK_SIZE_3D], n)
        assert virtual_data2.dtype == np.float64

def test_create_virtual_dataset_offset():
    with setup(version_name='test_version') as f:
        slices1 = write_dataset(f, 'test_data', np.ones((2*DEFAULT_CHUNK_SIZE,)))
        slices2 = write_dataset(f, 'test_data',
                                np.concatenate((2*np.ones((DEFAULT_CHUNK_SIZE,)),
                                                3*np.ones((DEFAULT_CHUNK_SIZE - 2,)))))

        virtual_data = create_virtual_dataset(f, 'test_version', 'test_data',
            {**slices1,
             Tuple(Slice(2*DEFAULT_CHUNK_SIZE, 3*DEFAULT_CHUNK_SIZE - 2),):
             slices2[(Slice(1*DEFAULT_CHUNK_SIZE, 2*DEFAULT_CHUNK_SIZE - 2),)]})

        assert virtual_data.shape == (3*DEFAULT_CHUNK_SIZE - 2,)
        assert_equal(virtual_data[0:2*DEFAULT_CHUNK_SIZE], 1.0)
        assert_equal(virtual_data[2*DEFAULT_CHUNK_SIZE:3*DEFAULT_CHUNK_SIZE - 2], 3.0)

def test_create_virtual_dataset_offset_multidimension():
    xfail()
    # TODO: Fix this test once this is implemented
    with setup(version_name='test_version') as f:
        slices1 = write_dataset(f, 'test_data', np.ones((2*DEFAULT_CHUNK_SIZE,)))
        slices2 = write_dataset(f, 'test_data',
                                np.concatenate((2*np.ones((DEFAULT_CHUNK_SIZE,)),
                                                3*np.ones((DEFAULT_CHUNK_SIZE - 2,)))))

        virtual_data = create_virtual_dataset(f, 'test_version', 'test_data',
                                              slices1 + [slices2[1]])

        assert virtual_data.shape == (3*DEFAULT_CHUNK_SIZE - 2,)
        assert_equal(virtual_data[0:2*DEFAULT_CHUNK_SIZE], 1.0)
        assert_equal(virtual_data[2*DEFAULT_CHUNK_SIZE:3*DEFAULT_CHUNK_SIZE - 2], 3.0)

def test_write_dataset_chunk_size():
    with setup() as f:
        chunk_size = 2**10
        chunks = (chunk_size,)
        slices1 = write_dataset(f, 'test_data', np.ones((2*chunk_size,)),
                                chunks=chunks)
        raises(ValueError, lambda: write_dataset(f, 'test_data',
            np.ones(chunks), chunks=(2**9,)))
        slices2 = write_dataset_chunks(f, 'test_data',
                                       {0: slices1[0],
                                        1: 2*np.ones(chunks),
                                        2: 2*np.ones(chunks),
                                        3: 3*np.ones(chunks),
                                       })

        assert slices1 == [slice(0*chunk_size, 1*chunk_size),
                           slice(0*chunk_size, 1*chunk_size)]
        assert slices2 == [slice(0*chunk_size, 1*chunk_size),
                           slice(1*chunk_size, 2*chunk_size),
                           slice(1*chunk_size, 2*chunk_size),
                           slice(2*chunk_size, 3*chunk_size)]

        ds = f['/_version_data/test_data/raw_data']
        assert ds.shape == (3*chunk_size,)
        assert_equal(ds[0:1*chunk_size], 1.0)
        assert_equal(ds[1*chunk_size:2*chunk_size], 2.0)
        assert_equal(ds[2*chunk_size:3*chunk_size], 3.0)
        assert_equal(ds[3*chunk_size:4*chunk_size], 0.0)
        assert ds.dtype == np.float64


def test_write_dataset_offset_chunk_size():
    with setup() as f:
        chunk_size = 2**10
        chunks = (chunk_size,)
        slices1 = write_dataset(f, 'test_data', np.ones((2*chunk_size,)), chunks=chunks)
        slices2 = write_dataset(f, 'test_data',
                                np.concatenate((2*np.ones(chunks),
                                                2*np.ones(chunks),
                                                3*np.ones((chunk_size - 2,)))))

        assert slices1 == [slice(0*chunk_size, 1*chunk_size),
                           slice(0*chunk_size, 1*chunk_size)]
        assert slices2 == [slice(1*chunk_size, 2*chunk_size),
                           slice(1*chunk_size, 2*chunk_size),
                           slice(2*chunk_size, 3*chunk_size - 2)]

        ds = f['/_version_data/test_data/raw_data']
        assert ds.shape == (3*chunk_size,)
        assert_equal(ds[0*chunk_size:1*chunk_size], 1.0)
        assert_equal(ds[1*chunk_size:2*chunk_size], 2.0)
        assert_equal(ds[2*chunk_size:3*chunk_size - 2], 3.0)
        assert_equal(ds[3*chunk_size-2:4*chunk_size], 0.0)

def test_write_dataset_compression():
    with setup() as f:
        slices1 = write_dataset(f, 'test_data',
                                np.ones((2*DEFAULT_CHUNK_SIZE,)),
                                compression='gzip', compression_opts=3)
        raises(ValueError, lambda: write_dataset(f, 'test_data',
            np.ones((DEFAULT_CHUNK_SIZE,)), compression='lzf'))
        raises(ValueError, lambda: write_dataset(f, 'test_data',
            np.ones((DEFAULT_CHUNK_SIZE,)), compression='gzip', compression_opts=4))

        assert slices1 == {
            (Slice(0*DEFAULT_CHUNK_SIZE, 1*DEFAULT_CHUNK_SIZE),):
                slice(0*DEFAULT_CHUNK_SIZE, 1*DEFAULT_CHUNK_SIZE),
            (Slice(1*DEFAULT_CHUNK_SIZE, 2*DEFAULT_CHUNK_SIZE),):
                slice(0*DEFAULT_CHUNK_SIZE, 1*DEFAULT_CHUNK_SIZE)}

        ds = f['/_version_data/test_data/raw_data']
        assert ds.shape == (1*DEFAULT_CHUNK_SIZE,)
        assert_equal(ds[0:1*DEFAULT_CHUNK_SIZE], 1.0)
        assert ds.dtype == np.float64
        assert ds.compression == 'gzip'
        assert ds.compression_opts == 3
