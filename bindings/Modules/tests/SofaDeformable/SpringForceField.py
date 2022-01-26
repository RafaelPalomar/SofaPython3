import unittest
import Sofa
from Sofa import SofaDeformable
import numpy as np


def create_scene(root):
    root.addObject("RequiredPlugin", name="SofaBaseMechanics")
    root.addObject("RequiredPlugin", name="SofaBaseTopology")

    # Create a simple plane having 3x3 nodes and a size of 3x3 on the yz plane centered on (-0.5,0,0).
    root.addChild('plane_1')
    root.plane_1.addObject('RegularGridTopology', name='grid', min=[-0.5, -1.5, -1.5], max=[-0.5, 1.5, 1.5], n=[1, 3, 3])
    root.plane_1.addObject('MechanicalObject', name='mo', template="Vec3d", position='@grid.position')

    # Create a simple plane having 3x3 nodes and a size of 3x3 on the yz plane centered on (0.5,0,0).
    root.addChild('plane_2')
    root.plane_2.addObject('RegularGridTopology', name='grid', min=[0.5, -1.5, -1.5], max=[0.5, 1.5, 1.5], n=[1, 3, 3])
    root.plane_2.addObject('MechanicalObject', name='mo', template="Vec3d", position='@grid.position')

    # Create a StiffSpringForceField between the two planes
    # WARNING: the object of type StiffSpringForceField is not created directly in root.
    # Its path is root.spring_ff.spring_ff
    root.addObject(
        'StiffSpringForceField',
        template='Vec3d',
        name='spring_ff',
        object1=root.plane_1.mo.getLinkPath(),
        object2=root.plane_2.mo.getLinkPath(),
        indices1=list(range(9)),
        indices2=list(range(9)),
        stiffness=1,
        damping=0,
        length=1.
    )


class Test(unittest.TestCase):
    def setUp(self) -> None:
        self.root = Sofa.Core.Node()
        create_scene(self.root)
        Sofa.Simulation.init(self.root)

    def tearDown(self) -> None:
        Sofa.Simulation.unload(self.root)
        self.root = None

    def test_get_springs(self):
        self.assertEqual(len(self.root.spring_ff.spring_ff.getSprings()), 9)
        for spring in self.root.spring_ff.spring_ff.getSprings():
            self.assertEqual(spring.springStiffness, 1.0)
            self.assertEqual(spring.dampingFactor, 0)
            self.assertEqual(spring.restLength, 1.)

    def test_remove_one_spring(self):
        self.assertEqual(len(self.root.spring_ff.spring_ff.getSprings()), 9)
        self.root.spring_ff.spring_ff.removeSpring(1)
        springs = self.root.spring_ff.spring_ff.getSprings()
        self.assertEqual(len(springs), 8)

    def test_remove_many_springs(self):
        self.assertEqual(len(self.root.spring_ff.spring_ff.getSprings()), 9)
        self.root.spring_ff.spring_ff.removeSprings([1, 2, 3])
        springs = self.root.spring_ff.spring_ff.getSprings()
        self.assertEqual(len(springs), 6)

    def test_clear(self):
        self.assertEqual(len(self.root.spring_ff.spring_ff.getSprings()), 9)
        self.root.spring_ff.spring_ff.clear()
        self.assertEqual(len(self.root.spring_ff.spring_ff.getSprings()), 0)

    def test_add_one_spring(self):
        self.root.spring_ff.spring_ff.clear()
        self.root.spring_ff.spring_ff.addSpring(
            SofaDeformable.LinearSpring(index1=2, index2=2, springStiffness=1, dampingFactor=1, restLength=1, elongationOnly=True, enabled=False)
        )
        self.assertEqual(len(self.root.spring_ff.spring_ff.getSprings()), 1)
        spring_1 = self.root.spring_ff.spring_ff.getSprings()[0]
        self.assertEqual(spring_1.index1, 2)
        self.assertEqual(spring_1.index2, 2)
        self.assertEqual(spring_1.springStiffness, 1)
        self.assertEqual(spring_1.dampingFactor, 1)
        self.assertEqual(spring_1.restLength, 1)
        self.assertTrue(spring_1.elongationOnly)
        self.assertFalse(spring_1.enabled)

        self.root.spring_ff.spring_ff.addSpring(index1=3, index2=3, springStiffness=2, dampingFactor=2, restLength=2)
        self.assertEqual(len(self.root.spring_ff.spring_ff.getSprings()), 2)
        spring_2 = self.root.spring_ff.spring_ff.getSprings()[1]
        self.assertEqual(spring_2.index1, 3)
        self.assertEqual(spring_2.index2, 3)
        self.assertEqual(spring_2.springStiffness, 2)
        self.assertEqual(spring_2.dampingFactor, 2)
        self.assertEqual(spring_2.restLength, 2)
        self.assertFalse(spring_2.elongationOnly)
        self.assertTrue(spring_2.enabled)

    def test_add_many_springs(self):
        self.root.spring_ff.spring_ff.clear()
        self.root.spring_ff.spring_ff.addSprings([
            SofaDeformable.LinearSpring(index1=2, index2=2, springStiffness=1, dampingFactor=1, restLength=1, elongationOnly=True, enabled=False),
            SofaDeformable.LinearSpring(index1=3, index2=3, springStiffness=2, dampingFactor=2, restLength=2, elongationOnly=False, enabled=True)
        ])
        self.assertEqual(len(self.root.spring_ff.spring_ff.getSprings()), 2)
        spring_1 = self.root.spring_ff.spring_ff.getSprings()[0]
        self.assertEqual(spring_1.index1, 2)
        self.assertEqual(spring_1.index2, 2)
        self.assertEqual(spring_1.springStiffness, 1)
        self.assertEqual(spring_1.dampingFactor, 1)
        self.assertEqual(spring_1.restLength, 1)
        self.assertTrue(spring_1.elongationOnly)
        self.assertFalse(spring_1.enabled)

        spring_2 = self.root.spring_ff.spring_ff.getSprings()[1]
        self.assertEqual(spring_2.index1, 3)
        self.assertEqual(spring_2.index2, 3)
        self.assertEqual(spring_2.springStiffness, 2)
        self.assertEqual(spring_2.dampingFactor, 2)
        self.assertEqual(spring_2.restLength, 2)
        self.assertFalse(spring_2.elongationOnly)
        self.assertTrue(spring_2.enabled)