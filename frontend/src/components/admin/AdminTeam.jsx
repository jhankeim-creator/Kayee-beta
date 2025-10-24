import React, { useState, useEffect, useContext } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '../ui/card';
import { Button } from '../ui/button';
import { Input } from '../ui/input';
import { Label } from '../ui/label';
import { Switch } from '../ui/switch';
import { toast } from 'sonner';
import axios from 'axios';
import { CartContext } from '../../App';
import { Plus, Trash2, Edit2, UserPlus, Shield, ShieldCheck } from 'lucide-react';

const AdminTeam = () => {
  const { API, token } = useContext(CartContext);
  const [teamMembers, setTeamMembers] = useState([]);
  const [loading, setLoading] = useState(false);
  const [showAddForm, setShowAddForm] = useState(false);
  const [editingMember, setEditingMember] = useState(null);

  const [formData, setFormData] = useState({
    email: '',
    password: '',
    name: '',
    is_super_admin: false,
    permissions: {
      manage_products: true,
      manage_orders: true,
      manage_customers: true,
      manage_coupons: true,
      manage_settings: true,
      manage_team: false
    }
  });

  useEffect(() => {
    loadTeamMembers();
  }, []);

  const loadTeamMembers = async () => {
    try {
      setLoading(true);
      const headers = { Authorization: `Bearer ${token}` };
      const res = await axios.get(`${API}/admin/team/members`, { headers });
      setTeamMembers(res.data);
    } catch (error) {
      console.error('Failed to load team members:', error);
      if (error.response?.status === 403) {
        toast.error("Vous n'avez pas la permission de gérer l'équipe");
      } else {
        toast.error('Échec du chargement des membres de l\'équipe');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!formData.email || !formData.name) {
      toast.error('Email et nom sont requis');
      return;
    }

    if (!editingMember && !formData.password) {
      toast.error('Le mot de passe est requis pour les nouveaux membres');
      return;
    }

    try {
      setLoading(true);
      const headers = { Authorization: `Bearer ${token}` };

      if (editingMember) {
        // Update existing member
        const updateData = {
          name: formData.name,
          permissions: formData.permissions
        };
        if (formData.password) {
          updateData.password = formData.password;
        }
        
        await axios.put(`${API}/admin/team/members/${editingMember.id}`, updateData, { headers });
        toast.success('Membre de l\'équipe mis à jour avec succès');
      } else {
        // Create new member
        await axios.post(`${API}/admin/team/members`, formData, { headers });
        toast.success('Nouveau membre ajouté avec succès');
      }

      resetForm();
      await loadTeamMembers();
    } catch (error) {
      console.error('Failed to save team member:', error);
      const errorMsg = error.response?.data?.detail || 'Échec de l\'enregistrement du membre';
      toast.error(errorMsg);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (memberId) => {
    if (!window.confirm('Are you sure you want to delete this member?')) {
      return;
    }

    try {
      setLoading(true);
      const headers = { Authorization: `Bearer ${token}` };
      await axios.delete(`${API}/admin/team/members/${memberId}`, { headers });
      toast.success('Membre supprimé avec succès');
      await loadTeamMembers();
    } catch (error) {
      console.error('Failed to delete team member:', error);
      const errorMsg = error.response?.data?.detail || 'Échec de la suppression du membre';
      toast.error(errorMsg);
    } finally {
      setLoading(false);
    }
  };

  const handleEdit = (member) => {
    setEditingMember(member);
    setFormData({
      email: member.email,
      password: '',
      name: member.name,
      is_super_admin: member.is_super_admin || false,
      permissions: member.permissions || {
        manage_products: true,
        manage_orders: true,
        manage_customers: true,
        manage_coupons: true,
        manage_settings: true,
        manage_team: false
      }
    });
    setShowAddForm(true);
  };

  const resetForm = () => {
    setFormData({
      email: '',
      password: '',
      name: '',
      is_super_admin: false,
      permissions: {
        manage_products: true,
        manage_orders: true,
        manage_customers: true,
        manage_coupons: true,
        manage_settings: true,
        manage_team: false
      }
    });
    setShowAddForm(false);
    setEditingMember(null);
  };

  const updatePermission = (key, value) => {
    setFormData({
      ...formData,
      permissions: {
        ...formData.permissions,
        [key]: value
      }
    });
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-2xl font-bold">Gestion d'Équipe Admin</h2>
          <p className="text-gray-600 mt-1">Gérer les utilisateurs admin et leurs permissions</p>
        </div>
        {!showAddForm && (
          <Button
            onClick={() => setShowAddForm(true)}
            className="bg-[#d4af37] hover:bg-[#b8941f]"
          >
            <UserPlus className="h-4 w-4 mr-2" />
            Ajouter un membre
          </Button>
        )}
      </div>

      {/* Add/Edit Form */}
      {showAddForm && (
        <Card>
          <CardHeader>
            <CardTitle>
              {editingMember ? 'Modifier le membre' : 'Ajouter un nouveau membre admin'}
            </CardTitle>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <Label>Email *</Label>
                  <Input
                    type="email"
                    value={formData.email}
                    onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                    placeholder="admin@example.com"
                    disabled={editingMember !== null}
                  />
                </div>
                <div>
                  <Label>Nom complet *</Label>
                  <Input
                    type="text"
                    value={formData.name}
                    onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                    placeholder="John Doe"
                  />
                </div>
              </div>

              <div>
                <Label>Mot de passe {editingMember ? '(laisser vide pour ne pas changer)' : '*'}</Label>
                <Input
                  type="password"
                  value={formData.password}
                  onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                  placeholder="********"
                />
              </div>

              <div className="border-t pt-4">
                <h3 className="font-semibold mb-4 flex items-center">
                  <Shield className="h-4 w-4 mr-2" />
                  Permissions
                </h3>
                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <div>
                      <Label>Super Admin</Label>
                      <p className="text-sm text-gray-500">Accès complet à toutes les fonctionnalités</p>
                    </div>
                    <Switch
                      checked={formData.is_super_admin}
                      onCheckedChange={(checked) => setFormData({ ...formData, is_super_admin: checked })}
                    />
                  </div>

                  {!formData.is_super_admin && (
                    <>
                      <div className="flex items-center justify-between">
                        <Label>Gérer les produits</Label>
                        <Switch
                          checked={formData.permissions.manage_products}
                          onCheckedChange={(checked) => updatePermission('manage_products', checked)}
                        />
                      </div>
                      <div className="flex items-center justify-between">
                        <Label>Gérer les commandes</Label>
                        <Switch
                          checked={formData.permissions.manage_orders}
                          onCheckedChange={(checked) => updatePermission('manage_orders', checked)}
                        />
                      </div>
                      <div className="flex items-center justify-between">
                        <Label>Gérer les clients</Label>
                        <Switch
                          checked={formData.permissions.manage_customers}
                          onCheckedChange={(checked) => updatePermission('manage_customers', checked)}
                        />
                      </div>
                      <div className="flex items-center justify-between">
                        <Label>Gérer les coupons</Label>
                        <Switch
                          checked={formData.permissions.manage_coupons}
                          onCheckedChange={(checked) => updatePermission('manage_coupons', checked)}
                        />
                      </div>
                      <div className="flex items-center justify-between">
                        <Label>Gérer les paramètres</Label>
                        <Switch
                          checked={formData.permissions.manage_settings}
                          onCheckedChange={(checked) => updatePermission('manage_settings', checked)}
                        />
                      </div>
                      <div className="flex items-center justify-between">
                        <Label>Gérer l'équipe</Label>
                        <Switch
                          checked={formData.permissions.manage_team}
                          onCheckedChange={(checked) => updatePermission('manage_team', checked)}
                        />
                      </div>
                    </>
                  )}
                </div>
              </div>

              <div className="flex gap-2">
                <Button
                  type="submit"
                  className="bg-[#d4af37] hover:bg-[#b8941f]"
                  disabled={loading}
                >
                  {loading ? 'Enregistrement...' : editingMember ? 'Mettre à jour' : 'Ajouter'}
                </Button>
                <Button type="button" variant="outline" onClick={resetForm}>
                  Annuler
                </Button>
              </div>
            </form>
          </CardContent>
        </Card>
      )}

      {/* Team Members List */}
      <Card>
        <CardHeader>
          <CardTitle>Membres de l'équipe ({teamMembers.length})</CardTitle>
        </CardHeader>
        <CardContent>
          {loading && !showAddForm ? (
            <div className="text-center py-8">
              <p className="text-gray-500">Chargement...</p>
            </div>
          ) : teamMembers.length === 0 ? (
            <div className="text-center py-8">
              <p className="text-gray-500">Aucun membre d'équipe trouvé</p>
            </div>
          ) : (
            <div className="space-y-4">
              {teamMembers.map((member) => (
                <div
                  key={member.id}
                  className="flex items-start justify-between p-4 border rounded hover:bg-gray-50"
                >
                  <div className="flex-1">
                    <div className="flex items-center gap-2 mb-1">
                      <h3 className="font-semibold text-lg">{member.name}</h3>
                      {member.is_super_admin && (
                        <span className="flex items-center gap-1 text-xs bg-[#d4af37] text-white px-2 py-1 rounded">
                          <ShieldCheck className="h-3 w-3" />
                          Super Admin
                        </span>
                      )}
                      {!member.is_active && (
                        <span className="text-xs bg-red-500 text-white px-2 py-1 rounded">
                          Inactif
                        </span>
                      )}
                    </div>
                    <p className="text-sm text-gray-600 mb-2">{member.email}</p>
                    
                    {!member.is_super_admin && member.permissions && (
                      <div className="flex flex-wrap gap-2 mt-2">
                        {member.permissions.manage_products && (
                          <span className="text-xs bg-blue-100 text-blue-700 px-2 py-1 rounded">
                            Produits
                          </span>
                        )}
                        {member.permissions.manage_orders && (
                          <span className="text-xs bg-green-100 text-green-700 px-2 py-1 rounded">
                            Commandes
                          </span>
                        )}
                        {member.permissions.manage_customers && (
                          <span className="text-xs bg-purple-100 text-purple-700 px-2 py-1 rounded">
                            Clients
                          </span>
                        )}
                        {member.permissions.manage_coupons && (
                          <span className="text-xs bg-yellow-100 text-yellow-700 px-2 py-1 rounded">
                            Coupons
                          </span>
                        )}
                        {member.permissions.manage_settings && (
                          <span className="text-xs bg-gray-100 text-gray-700 px-2 py-1 rounded">
                            Paramètres
                          </span>
                        )}
                        {member.permissions.manage_team && (
                          <span className="text-xs bg-red-100 text-red-700 px-2 py-1 rounded">
                            Équipe
                          </span>
                        )}
                      </div>
                    )}
                    
                    <p className="text-xs text-gray-400 mt-2">
                      Créé le: {new Date(member.created_at).toLocaleDateString('fr-FR')}
                    </p>
                  </div>

                  <div className="flex gap-2">
                    <Button
                      size="sm"
                      variant="outline"
                      onClick={() => handleEdit(member)}
                      disabled={loading}
                    >
                      <Edit2 className="h-4 w-4" />
                    </Button>
                    <Button
                      size="sm"
                      variant="destructive"
                      onClick={() => handleDelete(member.id)}
                      disabled={loading}
                    >
                      <Trash2 className="h-4 w-4" />
                    </Button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
};

export default AdminTeam;
